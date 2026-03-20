import os
import urllib.parse
from app import create_app, db
from models import Product

# Prevent starting the server, just init context
app = create_app()

with app.app_context():
    products = Product.query.all()
    count = 0
    for p in products:
        # Generate a distinct placeholder URL that explicitly contains the product name
        new_img = f"/api/placeholder/{urllib.parse.quote(p.name)}"
        
        # Avoid unnecessary writes if it's already updated
        if not p.image or p.image[0] != new_img:
            p.image = [new_img]
            count += 1
            
    db.session.commit()
    print(f"Updated images for {count} products to use unique matching placeholders.")
