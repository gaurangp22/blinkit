import os
import requests
import time
from duckduckgo_search import DDGS
from app import create_app, db
from models import Product

app = create_app()

def download_image(url, filename, upload_dir='/app/uploads'):
    try:
        # Use headers to bypass basic blocks
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            filepath = os.path.join(upload_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

with app.app_context():
    products = Product.query.all()
    upload_dir = '/app/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    
    ddgs = DDGS()
    
    count = 0
    print(f"Total products to process: {len(products)}")
    for p in products:
        # Only process if image is a placeholder or missing
        if not p.image or not p.image[0].startswith('/uploads/'):
            print(f"Searching for: {p.name}...")
            try:
                # Adding 'product India blinkit grofers' to get high quality relevant images
                query = f"{p.name} product India blinkit"
                results = list(ddgs.images(query, max_results=1))
                if results:
                    img_url = results[0]["image"]
                    print(f"Found image: {img_url}")
                    
                    # Ensure safe filename
                    safe_name = "".join(c if c.isalnum() else "_" for c in p.name)
                    ext = img_url.split('.')[-1].lower()
                    if len(ext) > 5 or '?' in ext or ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                        ext = 'jpg' # fallback
                    filename = f"img_{p.id}_{safe_name}.{ext}"
                    
                    if download_image(img_url, filename, upload_dir):
                        p.image = [f"/uploads/{filename}"]
                        db.session.commit()
                        count += 1
                        print(f"Successfully saved {p.name}")
                    else:
                        print(f"Failed to download, skipping: {p.name}")
                else:
                    print(f"No results for {p.name}")
            except Exception as e:
                print(f"Rate limit or error searching for {p.name}: {e}")
                time.sleep(2) # Back off on error
                
            time.sleep(0.5) # Prevent aggressive rate limiting
            
    print(f"Finished! Successfully downloaded and updated {count} product images.")
