import os
import json
import time
import requests
from app import create_app, db
from models import Product

app = create_app()

API_KEY = "3d28c9a378b375b1455e33da641e179fe6ac9218"

def search_serper_images(query):
    url = "https://google.serper.dev/images"
    payload = json.dumps({"q": query})
    headers = {'X-API-KEY': API_KEY, 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        data = response.json()
        if "images" in data:
            return [img.get("imageUrl") for img in data["images"] if img.get("imageUrl")]
    except Exception as e:
        print(f"Serper API error: {e}")
    return []

def download_image(url, filename, upload_dir='/app/uploads'):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
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
    
    # Process only records that don't have an upload yet
    missing_products = [p for p in products if not p.image or not p.image[0].startswith('/uploads/')]
    print(f"Retrying download for {len(missing_products)} missing products...")
    
    for p in missing_products:
        print(f"Retrying: {p.name}...")
        try:
            query = f"{p.name} blinkit product packaging"
            urls = search_serper_images(query)
            
            success = False
            for img_url in urls[:5]: # Try up to 5 fallback images
                safe_name = "".join(c if c.isalnum() else "_" for c in p.name)
                ext = img_url.split('/')[-1].split('?')[0].split('.')[-1].lower()
                if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                    ext = 'jpg'
                filename = f"serp_retry_{p.id}_{safe_name[:15]}.{ext}"
                
                if download_image(img_url, filename, upload_dir):
                    p.image = [f"/uploads/{filename}"]
                    db.session.commit()
                    count += 1
                    print(f"  Successfully saved {p.name} on fallback!")
                    success = True
                    break
            
            if not success:
                print(f"  All 5 fallback attempts failed for: {p.name}")
        except Exception as e:
            print(f"  Crashed searching for {p.name}: {e}")
            
        time.sleep(0.1)

    print(f"\nFinished retry execution! Found {count} missing images.")
