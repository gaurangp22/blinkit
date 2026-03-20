import os
import re
import time
import requests
from app import create_app, db
from models import Product

app = create_app()

def search_bing_image(query):
    url = f"https://www.bing.com/images/search?q={requests.utils.quote(query)}&first=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        # Bing stores the high resolution image URL in the block like "murl":"https://something.jpg"
        matches = re.finditer(r'"murl":"([^"]+)"', res.text)
        for match in matches:
            img_url = match.group(1)
            # Some domains block hotlinking/scraping, avoid them or just attempt first 3
            if img_url.endswith('.jpg') or img_url.endswith('.png') or img_url.endswith('.webp'):
                return img_url
        
        # fallback if no extension match but found murl
        fallback_match = re.search(r'"murl":"([^"]+)"', res.text)
        if fallback_match:
            return fallback_match.group(1)
            
    except Exception as e:
        print(f"Error fetching Bing: {e}")
    return None

def download_image(url, filename, upload_dir='/app/uploads'):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            filepath = os.path.join(upload_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except Exception:
        pass
    return False

with app.app_context():
    products = Product.query.all()
    upload_dir = '/app/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    count = 0
    print(f"Total products to process: {len(products)}")
    
    for p in products:
        if not p.image or not p.image[0].startswith('/uploads/'):
            print(f"Searching for: {p.name}...")
            try:
                # Add 'product packaging' and 'grocery' context to improve accuracy
                query = f"{p.name} blinkit product packaging"
                img_url = search_bing_image(query)
                if img_url:
                    print(f"  Found image: {img_url[:60]}...")
                    safe_name = "".join(c if c.isalnum() else "_" for c in p.name)
                    
                    ext = img_url.split('/')[-1].split('?')[0].split('.')[-1].lower()
                    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                        ext = 'jpg'
                    filename = f"bing_{p.id}_{safe_name[:15]}.{ext}"
                    
                    if download_image(img_url, filename, upload_dir):
                        p.image = [f"/uploads/{filename}"]
                        db.session.commit()
                        count += 1
                        print(f"  Successfully saved {p.name}!")
                    else:
                        print(f"  Failed image download: {p.name}")
                else:
                    print(f"  No Bing results for {p.name}")
            except Exception as e:
                print(f"  Crashed searching for {p.name}: {e}")
                
            time.sleep(0.5)

    print(f"\nFinished scraping via Bing! Successfully updated {count} images in the DB.")
