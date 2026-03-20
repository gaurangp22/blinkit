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
        if response.status_code == 200 and len(response.content) > 1000:
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
    
    missing = [p for p in products if not p.image or not p.image[0].startswith('/uploads/')]
    print(f"Final pass for {len(missing)} missing products...")
    
    for p in missing:
        print(f"Final try: {p.name}...")
        # Use simpler search terms, strip weight/size info
        simple_name = p.name.split(' ')[0] + ' ' + (' '.join(p.name.split(' ')[1:3]) if len(p.name.split(' ')) > 1 else '')
        
        queries = [
            f"{p.name} product image",
            f"{simple_name} product",
            f"{p.name} grocery",
        ]
        
        success = False
        for query in queries:
            urls = search_serper_images(query)
            for img_url in urls[:3]:
                safe_name = "".join(c if c.isalnum() else "_" for c in p.name)
                filename = f"final_{p.id}_{safe_name[:15]}.jpg"
                if download_image(img_url, filename, upload_dir):
                    p.image = [f"/uploads/{filename}"]
                    db.session.commit()
                    count += 1
                    print(f"  Got it: {p.name}!")
                    success = True
                    break
            if success:
                break
        
        if not success:
            print(f"  Still failed: {p.name}")
        time.sleep(0.1)

    print(f"\nFinal pass done! Fixed {count} more images.")
