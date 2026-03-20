import os
import json
import time
import requests
from app import create_app, db
from models import Product

app = create_app()

API_KEY = "3d28c9a378b375b1455e33da641e179fe6ac9218"

def search_serper_image(query):
    url = "https://google.serper.dev/images"
    payload = json.dumps({
      "q": query
    })
    headers = {
      'X-API-KEY': API_KEY,
      'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        data = response.json()
        if "images" in data and len(data["images"]) > 0:
            for img in data["images"]:
                img_url = img.get("imageUrl")
                if img_url:
                    # Skip extremely large images or PDF/SVGs if possible, but first one is usually fine
                    return img_url
    except Exception as e:
        print(f"Serper API error: {e}")
    return None

def download_image(url, filename, upload_dir='/app/uploads'):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
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
            print(f"Searching Serper for: {p.name}...")
            try:
                # Add 'grocery India product' to improve accuracy
                query = f"{p.name} grocery India product white background"
                img_url = search_serper_image(query)
                if img_url:
                    print(f"  Found image: {img_url[:60]}...")
                    safe_name = "".join(c if c.isalnum() else "_" for c in p.name)
                    
                    ext = img_url.split('/')[-1].split('?')[0].split('.')[-1].lower()
                    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                        ext = 'jpg'
                    filename = f"serp_{p.id}_{safe_name[:15]}.{ext}"
                    
                    if download_image(img_url, filename, upload_dir):
                        p.image = [f"/uploads/{filename}"]
                        db.session.commit()
                        count += 1
                        print(f"  Successfully saved {p.name}!")
                    else:
                        print(f"  Failed image download: {p.name}")
                else:
                    print(f"  No Serper results for {p.name}")
            except Exception as e:
                print(f"  Crashed searching for {p.name}: {e}")
                
            time.sleep(0.1) # Safe to be faster with official API

    print(f"\nFinished scraping via Serper! Successfully updated {count} images in the DB.")
