import os
import bcrypt
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from config import Config
from models import db, User, Category, SubCategory, Product


def seed_users():
    """Create default admin and user accounts if they don't exist."""
    # Admin account
    if not User.query.filter_by(email="admin@cartify.com").first():
        hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        admin = User(
            name="Admin",
            email="admin@cartify.com",
            password=hashed,
            mobile="9999999999",
            role="ADMIN",
            status="Active",
        )
        db.session.add(admin)
        print("Created admin account: admin@cartify.com / admin123")

    # Regular user account
    if not User.query.filter_by(email="user@cartify.com").first():
        hashed = bcrypt.hashpw("user123".encode(), bcrypt.gensalt()).decode()
        user = User(
            name="Bharvi",
            email="user@cartify.com",
            password=hashed,
            mobile="8888888888",
            role="USER",
            status="Active",
        )
        db.session.add(user)
        print("Created user account: user@cartify.com / user123")

    db.session.commit()


def seed_data():
    """Seed categories, subcategories, and products when the database is empty."""
    if Category.query.count() > 0:
        print("Seed data already exists, skipping.")
        return

    # ── Categories (all 20) ─────────────────────────────────────────
    categories_data = {
        "Fruits & Vegetables": "/categories/fruits-&-vegetables.png",
        "Dairy, Bread & Eggs": "/categories/dairy-bread-&-eggs.png",
        "Snacks & Munchies": "/categories/snacks-&-munchies.png",
        "Cold Drinks & Juices": "/categories/cold-drinks-&-juices.png",
        "Breakfast & Instant Food": "/categories/breakfast-&-instant-food.png",
        "Bakery & Biscuits": "/categories/bakery-&-biscuits.png",
        "Atta, Rice & Dal": "/categories/atta-rice-&-dal.png",
        "Masala, Oil & More": "/categories/masala-oil-&-more.png",
        "Sauces & Spreads": "/categories/sauces-&-spreads.png",
        "Personal Care": "/categories/personal-care.png",
        "Cleaning Essentials": "/categories/cleaning-essentials.png",
        "Home & Office": "/categories/home-&-office.png",
        "Tea, Coffee & Health Drink": "/categories/tea-coffe-&-health-drink.png",
        "Sweet Tooth": "/categories/sweet-tooth.png",
        "Baby Care": "/categories/baby-care.png",
        "Pet Care": "/categories/pet-care.png",
        "Pharma & Wellness": "/categories/pharma-&-wellness.png",
        "Chicken, Meat & Fish": "/categories/chicken-meat-&-fish.png",
        "Organic & Healthy Living": "/categories/organic-&-healthy-living.png",
        "Paan Corner": "/categories/paan-corner.png",
    }

    categories = {}
    for name, image in categories_data.items():
        cat = Category(name=name, image=image)
        db.session.add(cat)
        categories[name] = cat

    db.session.flush()

    # ── SubCategories ───────────────────────────────────────────────
    # { category_name: [ (subcategory_name, image_path), ... ] }
    subcategories_map = {
        "Fruits & Vegetables": [
            ("Fresh Fruits", "/subcategories/dry-fruits.webp"),
            ("Fresh Vegetables", "/subcategories/oil.webp"),
        ],
        "Dairy, Bread & Eggs": [
            ("Milk", "/subcategories/milk.webp"),
            ("Curd & Yogurt", "/subcategories/curd-&-yogurt.jpg"),
            ("Bread & Pav", "/subcategories/bread-&-pav.webp"),
            ("Eggs", "/subcategories/eggs.webp"),
            ("Cheese", "/subcategories/cheese.webp"),
            ("Butter & More", "/subcategories/butter-&-more.webp"),
            ("Paneer & Tofu", "/subcategories/paneer-&-tofu.webp"),
        ],
        "Snacks & Munchies": [
            ("Chips & Crisps", "/subcategories/chips-&-crisps.webp"),
            ("Bhujia & Mixtures", "/subcategories/bhujia-&-mixtures.webp"),
            ("Namkeen Snacks", "/subcategories/namkeen-snacks.webp"),
        ],
        "Cold Drinks & Juices": [
            ("Soft Drinks", "/subcategories/soft-drinks.webp"),
            ("Fruit Juices", "/subcategories/fruit-juices.webp"),
            ("Energy Drinks", "/subcategories/energy-drinks.webp"),
        ],
        "Breakfast & Instant Food": [
            ("Noodles", "/subcategories/noodles.webp"),
            ("Pasta", "/subcategories/pasta.webp"),
            ("Oats", "/subcategories/oats.webp"),
        ],
        "Bakery & Biscuits": [
            ("Cookies", "/subcategories/cookies.webp"),
            ("Cream Biscuits", "/subcategories/cream-biscuits.webp"),
            ("Glucose & Marie", "/subcategories/glucose-&-marie.webp"),
        ],
        "Atta, Rice & Dal": [
            ("Salt, Sugar & Jaggery", "/subcategories/salt-sugar-&-jaggery.webp"),
        ],
        "Masala, Oil & More": [
            ("Oil", "/subcategories/oil.webp"),
            ("Ghee & Vanaspati", "/subcategories/ghee-&-vanaspati.webp"),
            ("Powdered Spices", "/subcategories/powdered-spices.webp"),
        ],
        "Sauces & Spreads": [
            ("Tomato & Chilli Ketchup", "/subcategories/tomato-&-chilli-ketchup.webp"),
            ("Jam & Spreads", "/subcategories/jam-&-spreads.webp"),
            ("Indian Chutney & Pickle", "/subcategories/indian-chutney-&-pickle.webp"),
        ],
        "Personal Care": [
            ("Bathing Soaps", "/subcategories/bathing-soaps.webp"),
            ("Shampoo & Conditioner", "/subcategories/shampoo-&-conditioner.webp"),
            ("Face Care", "/subcategories/face-care.png"),
        ],
        "Cleaning Essentials": [
            ("Detergent Powder & Bars", "/subcategories/detergent-powder-&-bars.webp"),
            ("Floor Cleaners & More", "/subcategories/floor-cleaners-&-more.webp"),
            ("Dishwashing Bars", "/subcategories/dishwashing-bars.webp"),
        ],
        "Home & Office": [
            ("Kitchen & Dining Needs", "/subcategories/kitchen-&-dining-needs.webp"),
            ("Stationery Needs", "/subcategories/stationery-needs.webp"),
            ("Appliances", "/subcategories/appliances.webp"),
        ],
        "Tea, Coffee & Health Drink": [
            ("Tea", "/subcategories/tea.webp"),
            ("Coffee", "/subcategories/coffee.jpg"),
            ("Green & Flavoured Tea", "/subcategories/green-&-flavoured-tea.webp"),
        ],
        "Sweet Tooth": [
            ("Chocolates", "/subcategories/chocolates.png"),
            ("Ice Cream & Frozen Dessert", "/subcategories/ice-cream-&-frozen-dessert.webp"),
            ("Indian Sweets", "/subcategories/indian-sweets.webp"),
        ],
        "Baby Care": [
            ("Baby Food", "/subcategories/baby-food.webp"),
        ],
        "Pet Care": [
            ("Dog Needs", "/subcategories/dog-needs.png"),
            ("Cat Needs", "/subcategories/cat-needs.png"),
        ],
        "Pharma & Wellness": [
            ("Everyday Medicines", "/subcategories/everyday-medicines.webp"),
            ("Vitamins & Daily Nutrition", "/subcategories/vitamins-&-daily-nutrition.webp"),
            ("Cough & Cold", "/subcategories/cough-&-cold.webp"),
        ],
        "Chicken, Meat & Fish": [
            ("Chicken", "/subcategories/chicken.jpg"),
            ("Fish & Seafood", "/subcategories/fish-&-seafood.jpg"),
            ("Sausage, Salami & Ham", "/subcategories/sausage-salami-&-ham.webp"),
        ],
        "Organic & Healthy Living": [
            ("Dry Fruits", "/subcategories/dry-fruits.webp"),
            ("Healthy Proteins", "/subcategories/healthy-proteins.webp"),
        ],
        "Paan Corner": [
            ("Paan", "/subcategories/paan.webp"),
            ("Mouth Fresheners", "/subcategories/mouth-fresheners.webp"),
        ],
    }

    subcategories = {}
    for cat_name, sub_list in subcategories_map.items():
        for sub_name, sub_image in sub_list:
            sub = SubCategory(name=sub_name, image=sub_image)
            sub.category.append(categories[cat_name])
            db.session.add(sub)
            subcategories[sub_name] = sub

    db.session.flush()

    # ── Products ────────────────────────────────────────────────────
    products_data = [
        # ─── Fruits & Vegetables ────────────────────────────────────
        {"name": "Fresh Banana (1 dozen)", "description": "Ripe yellow bananas, rich in potassium", "unit": "1 dozen", "stock": 150, "price": 40, "discount": 5, "cat": "Fruits & Vegetables", "sub": "Fresh Fruits", "image": "/subcategories/dry-fruits.webp"},
        {"name": "Shimla Apple 1kg", "description": "Crisp and juicy Himachali apples", "unit": "1 kg", "stock": 100, "price": 180, "discount": 10, "cat": "Fruits & Vegetables", "sub": "Fresh Fruits", "image": "/subcategories/dry-fruits.webp"},
        {"name": "Alphonso Mango 1kg", "description": "Premium Ratnagiri Alphonso mangoes", "unit": "1 kg", "stock": 60, "price": 450, "discount": 0, "cat": "Fruits & Vegetables", "sub": "Fresh Fruits", "image": "/subcategories/dry-fruits.webp"},
        {"name": "Fresh Tomato 1kg", "description": "Farm-fresh red tomatoes for curries and salads", "unit": "1 kg", "stock": 200, "price": 30, "discount": 0, "cat": "Fruits & Vegetables", "sub": "Fresh Vegetables", "image": "/subcategories/oil.webp"},
        {"name": "Onion 1kg", "description": "Premium quality onions, a kitchen staple", "unit": "1 kg", "stock": 200, "price": 35, "discount": 0, "cat": "Fruits & Vegetables", "sub": "Fresh Vegetables", "image": "/subcategories/oil.webp"},
        {"name": "Green Capsicum 500g", "description": "Crunchy capsicum for stir-fries and salads", "unit": "500 g", "stock": 120, "price": 45, "discount": 0, "cat": "Fruits & Vegetables", "sub": "Fresh Vegetables", "image": "/subcategories/oil.webp"},

        # ─── Dairy, Bread & Eggs ────────────────────────────────────
        {"name": "Amul Taza Milk 1L", "description": "Fresh toned milk", "unit": "1 litre", "stock": 200, "price": 54, "discount": 0, "cat": "Dairy, Bread & Eggs", "sub": "Milk", "image": "/subcategories/milk.webp"},
        {"name": "Mother Dairy Full Cream 1L", "description": "Rich full cream milk for tea and sweets", "unit": "1 litre", "stock": 150, "price": 68, "discount": 0, "cat": "Dairy, Bread & Eggs", "sub": "Milk", "image": "/subcategories/milk.webp"},
        {"name": "Amul Masti Dahi 400g", "description": "Thick and creamy fresh curd", "unit": "400 g", "stock": 100, "price": 35, "discount": 5, "cat": "Dairy, Bread & Eggs", "sub": "Curd & Yogurt", "image": "/subcategories/curd-&-yogurt.jpg"},
        {"name": "Epigamia Greek Yogurt 90g", "description": "Protein-rich Greek yogurt, strawberry flavour", "unit": "90 g", "stock": 80, "price": 45, "discount": 0, "cat": "Dairy, Bread & Eggs", "sub": "Curd & Yogurt", "image": "/subcategories/curd-&-yogurt.jpg"},
        {"name": "Harvest Gold White Bread", "description": "Soft and fresh white sandwich bread", "unit": "400 g", "stock": 120, "price": 40, "discount": 0, "cat": "Dairy, Bread & Eggs", "sub": "Bread & Pav", "image": "/subcategories/bread-&-pav.webp"},
        {"name": "Amul Pav 6 pcs", "description": "Soft ladi pav, perfect for pav bhaji", "unit": "6 pcs", "stock": 90, "price": 35, "discount": 0, "cat": "Dairy, Bread & Eggs", "sub": "Bread & Pav", "image": "/subcategories/bread-&-pav.webp"},
        {"name": "Brown Country Eggs (6 pcs)", "description": "Farm-fresh protein-rich eggs", "unit": "6 pcs", "stock": 180, "price": 60, "discount": 0, "cat": "Dairy, Bread & Eggs", "sub": "Eggs", "image": "/subcategories/eggs.webp"},
        {"name": "Amul Cheese Slices 100g", "description": "Processed cheese slices for sandwiches", "unit": "100 g", "stock": 100, "price": 85, "discount": 5, "cat": "Dairy, Bread & Eggs", "sub": "Cheese", "image": "/subcategories/cheese.webp"},

        # ─── Snacks & Munchies ──────────────────────────────────────
        {"name": "Lays Classic Salted 52g", "description": "Crispy classic salted potato chips", "unit": "52 g", "stock": 200, "price": 20, "discount": 0, "cat": "Snacks & Munchies", "sub": "Chips & Crisps", "image": "/subcategories/chips-&-crisps.webp"},
        {"name": "Bingo Mad Angles 72.5g", "description": "Tangy tomato flavoured triangle chips", "unit": "72.5 g", "stock": 150, "price": 20, "discount": 0, "cat": "Snacks & Munchies", "sub": "Chips & Crisps", "image": "/subcategories/chips-&-crisps.webp"},
        {"name": "Kurkure Masala Munch 90g", "description": "Crunchy spicy puffed corn snack", "unit": "90 g", "stock": 180, "price": 20, "discount": 0, "cat": "Snacks & Munchies", "sub": "Chips & Crisps", "image": "/subcategories/chips-&-crisps.webp"},
        {"name": "Haldiram Aloo Bhujia 200g", "description": "Crunchy and spicy aloo bhujia", "unit": "200 g", "stock": 100, "price": 55, "discount": 10, "cat": "Snacks & Munchies", "sub": "Bhujia & Mixtures", "image": "/subcategories/bhujia-&-mixtures.webp"},
        {"name": "Haldiram Navratan Mixture 200g", "description": "Classic savoury mix of nuts and lentils", "unit": "200 g", "stock": 100, "price": 60, "discount": 5, "cat": "Snacks & Munchies", "sub": "Bhujia & Mixtures", "image": "/subcategories/bhujia-&-mixtures.webp"},
        {"name": "Bikaji Bikaneri Bhujia 400g", "description": "Authentic Rajasthani bhujia", "unit": "400 g", "stock": 80, "price": 110, "discount": 10, "cat": "Snacks & Munchies", "sub": "Namkeen Snacks", "image": "/subcategories/namkeen-snacks.webp"},

        # ─── Cold Drinks & Juices ───────────────────────────────────
        {"name": "Coca Cola 750ml", "description": "Chilled refreshing cola drink", "unit": "750 ml", "stock": 150, "price": 40, "discount": 0, "cat": "Cold Drinks & Juices", "sub": "Soft Drinks", "image": "/subcategories/soft-drinks.webp"},
        {"name": "Sprite 750ml", "description": "Lemon-lime clear soft drink", "unit": "750 ml", "stock": 140, "price": 40, "discount": 0, "cat": "Cold Drinks & Juices", "sub": "Soft Drinks", "image": "/subcategories/soft-drinks.webp"},
        {"name": "Thums Up 750ml", "description": "Bold and strong cola taste", "unit": "750 ml", "stock": 130, "price": 40, "discount": 0, "cat": "Cold Drinks & Juices", "sub": "Soft Drinks", "image": "/subcategories/soft-drinks.webp"},
        {"name": "Tropicana Orange Juice 1L", "description": "100% pure orange juice, no added sugar", "unit": "1 litre", "stock": 80, "price": 110, "discount": 10, "cat": "Cold Drinks & Juices", "sub": "Fruit Juices", "image": "/subcategories/fruit-juices.webp"},
        {"name": "Real Mango Juice 1L", "description": "Rich Alphonso mango juice", "unit": "1 litre", "stock": 75, "price": 99, "discount": 15, "cat": "Cold Drinks & Juices", "sub": "Fruit Juices", "image": "/subcategories/fruit-juices.webp"},
        {"name": "Red Bull Energy Drink 250ml", "description": "Energy drink that gives you wings", "unit": "250 ml", "stock": 60, "price": 125, "discount": 0, "cat": "Cold Drinks & Juices", "sub": "Energy Drinks", "image": "/subcategories/energy-drinks.webp"},

        # ─── Breakfast & Instant Food ───────────────────────────────
        {"name": "Maggi 2-Minute Noodles (4 pack)", "description": "India's favourite instant noodles", "unit": "4 x 70 g", "stock": 200, "price": 56, "discount": 0, "cat": "Breakfast & Instant Food", "sub": "Noodles", "image": "/subcategories/noodles.webp"},
        {"name": "Yippee Noodles Magic Masala", "description": "Round block noodles with magic masala", "unit": "70 g", "stock": 180, "price": 14, "discount": 0, "cat": "Breakfast & Instant Food", "sub": "Noodles", "image": "/subcategories/noodles.webp"},
        {"name": "Disano Penne Pasta 500g", "description": "Durum wheat semolina penne rigate", "unit": "500 g", "stock": 90, "price": 99, "discount": 10, "cat": "Breakfast & Instant Food", "sub": "Pasta", "image": "/subcategories/pasta.webp"},
        {"name": "Quaker Oats 1kg", "description": "Whole grain rolled oats for healthy breakfast", "unit": "1 kg", "stock": 100, "price": 199, "discount": 15, "cat": "Breakfast & Instant Food", "sub": "Oats", "image": "/subcategories/oats.webp"},

        # ─── Bakery & Biscuits ──────────────────────────────────────
        {"name": "Britannia Good Day Cookies 200g", "description": "Butter cashew cookies", "unit": "200 g", "stock": 150, "price": 40, "discount": 5, "cat": "Bakery & Biscuits", "sub": "Cookies", "image": "/subcategories/cookies.webp"},
        {"name": "Sunfeast Dark Fantasy 100g", "description": "Choco-filled premium cookies", "unit": "100 g", "stock": 120, "price": 40, "discount": 0, "cat": "Bakery & Biscuits", "sub": "Cookies", "image": "/subcategories/cookies.webp"},
        {"name": "Oreo Vanilla Cream Biscuit 120g", "description": "Chocolate biscuit with vanilla cream", "unit": "120 g", "stock": 180, "price": 30, "discount": 0, "cat": "Bakery & Biscuits", "sub": "Cream Biscuits", "image": "/subcategories/cream-biscuits.webp"},
        {"name": "Parle-G Glucose Biscuit 250g", "description": "India's most loved glucose biscuit", "unit": "250 g", "stock": 200, "price": 25, "discount": 5, "cat": "Bakery & Biscuits", "sub": "Glucose & Marie", "image": "/subcategories/glucose-&-marie.webp"},

        # ─── Atta, Rice & Dal ───────────────────────────────────────
        {"name": "Aashirvaad Atta 5kg", "description": "Whole wheat flour for soft rotis", "unit": "5 kg", "stock": 80, "price": 295, "discount": 10, "cat": "Atta, Rice & Dal", "sub": "Salt, Sugar & Jaggery", "image": "/subcategories/salt-sugar-&-jaggery.webp"},
        {"name": "India Gate Basmati Rice 5kg", "description": "Premium aged basmati rice", "unit": "5 kg", "stock": 60, "price": 499, "discount": 15, "cat": "Atta, Rice & Dal", "sub": "Salt, Sugar & Jaggery", "image": "/subcategories/salt-sugar-&-jaggery.webp"},
        {"name": "Tata Salt 1kg", "description": "Vacuum evaporated iodised salt", "unit": "1 kg", "stock": 200, "price": 28, "discount": 0, "cat": "Atta, Rice & Dal", "sub": "Salt, Sugar & Jaggery", "image": "/subcategories/salt-sugar-&-jaggery.webp"},

        # ─── Masala, Oil & More ─────────────────────────────────────
        {"name": "Fortune Sunflower Oil 1L", "description": "Light and healthy refined sunflower oil", "unit": "1 litre", "stock": 100, "price": 155, "discount": 10, "cat": "Masala, Oil & More", "sub": "Oil", "image": "/subcategories/oil.webp"},
        {"name": "Saffola Gold Oil 1L", "description": "Blended edible vegetable oil", "unit": "1 litre", "stock": 90, "price": 189, "discount": 5, "cat": "Masala, Oil & More", "sub": "Oil", "image": "/subcategories/oil.webp"},
        {"name": "Amul Pure Ghee 500ml", "description": "Pure cow ghee made from fresh cream", "unit": "500 ml", "stock": 80, "price": 295, "discount": 0, "cat": "Masala, Oil & More", "sub": "Ghee & Vanaspati", "image": "/subcategories/ghee-&-vanaspati.webp"},
        {"name": "MDH Chana Masala 100g", "description": "Authentic blend of spices for chana", "unit": "100 g", "stock": 120, "price": 68, "discount": 0, "cat": "Masala, Oil & More", "sub": "Powdered Spices", "image": "/subcategories/powdered-spices.webp"},
        {"name": "Everest Garam Masala 100g", "description": "Aromatic garam masala blend", "unit": "100 g", "stock": 110, "price": 85, "discount": 5, "cat": "Masala, Oil & More", "sub": "Powdered Spices", "image": "/subcategories/powdered-spices.webp"},

        # ─── Sauces & Spreads ───────────────────────────────────────
        {"name": "Kissan Tomato Ketchup 500g", "description": "Made with 100% real tomatoes", "unit": "500 g", "stock": 120, "price": 105, "discount": 10, "cat": "Sauces & Spreads", "sub": "Tomato & Chilli Ketchup", "image": "/subcategories/tomato-&-chilli-ketchup.webp"},
        {"name": "Maggi Hot & Sweet Sauce 500g", "description": "Sweet and spicy tomato chilli sauce", "unit": "500 g", "stock": 100, "price": 115, "discount": 5, "cat": "Sauces & Spreads", "sub": "Tomato & Chilli Ketchup", "image": "/subcategories/tomato-&-chilli-ketchup.webp"},
        {"name": "Kissan Mixed Fruit Jam 500g", "description": "Delicious mixed fruit jam for breakfast", "unit": "500 g", "stock": 90, "price": 155, "discount": 10, "cat": "Sauces & Spreads", "sub": "Jam & Spreads", "image": "/subcategories/jam-&-spreads.webp"},
        {"name": "Priya Mango Pickle 300g", "description": "Traditional Andhra mango pickle", "unit": "300 g", "stock": 80, "price": 89, "discount": 0, "cat": "Sauces & Spreads", "sub": "Indian Chutney & Pickle", "image": "/subcategories/indian-chutney-&-pickle.webp"},

        # ─── Personal Care ──────────────────────────────────────────
        {"name": "Dove Cream Beauty Bar 100g", "description": "Moisturizing soap with 1/4 cream", "unit": "100 g", "stock": 120, "price": 55, "discount": 5, "cat": "Personal Care", "sub": "Bathing Soaps", "image": "/subcategories/bathing-soaps.webp"},
        {"name": "Dettol Original Soap 125g", "description": "Antibacterial bath soap for germ protection", "unit": "125 g", "stock": 150, "price": 42, "discount": 0, "cat": "Personal Care", "sub": "Bathing Soaps", "image": "/subcategories/bathing-soaps.webp"},
        {"name": "Head & Shoulders Shampoo 340ml", "description": "Anti-dandruff shampoo for flake-free hair", "unit": "340 ml", "stock": 70, "price": 250, "discount": 10, "cat": "Personal Care", "sub": "Shampoo & Conditioner", "image": "/subcategories/shampoo-&-conditioner.webp"},
        {"name": "Himalaya Neem Face Wash 150ml", "description": "Purifying neem face wash for acne control", "unit": "150 ml", "stock": 90, "price": 160, "discount": 10, "cat": "Personal Care", "sub": "Face Care", "image": "/subcategories/face-care.png"},

        # ─── Cleaning Essentials ────────────────────────────────────
        {"name": "Surf Excel Easy Wash 1kg", "description": "Powerful stain remover detergent powder", "unit": "1 kg", "stock": 100, "price": 120, "discount": 10, "cat": "Cleaning Essentials", "sub": "Detergent Powder & Bars", "image": "/subcategories/detergent-powder-&-bars.webp"},
        {"name": "Rin Advanced Bar 250g", "description": "Detergent bar for sparkling white clothes", "unit": "250 g", "stock": 150, "price": 25, "discount": 0, "cat": "Cleaning Essentials", "sub": "Detergent Powder & Bars", "image": "/subcategories/detergent-powder-&-bars.webp"},
        {"name": "Lizol Floor Cleaner 500ml", "description": "Disinfectant surface cleaner kills 99.9% germs", "unit": "500 ml", "stock": 80, "price": 115, "discount": 5, "cat": "Cleaning Essentials", "sub": "Floor Cleaners & More", "image": "/subcategories/floor-cleaners-&-more.webp"},
        {"name": "Vim Dishwash Bar 300g", "description": "Tough on grease, gentle on hands", "unit": "300 g", "stock": 120, "price": 30, "discount": 0, "cat": "Cleaning Essentials", "sub": "Dishwashing Bars", "image": "/subcategories/dishwashing-bars.webp"},

        # ─── Home & Office ──────────────────────────────────────────
        {"name": "Milton Steel Flask 500ml", "description": "Stainless steel vacuum flask", "unit": "1 pc", "stock": 50, "price": 499, "discount": 15, "cat": "Home & Office", "sub": "Kitchen & Dining Needs", "image": "/subcategories/kitchen-&-dining-needs.webp"},
        {"name": "Borosil Lunch Box 400ml", "description": "Microwave-safe glass lunch box", "unit": "1 pc", "stock": 60, "price": 399, "discount": 10, "cat": "Home & Office", "sub": "Kitchen & Dining Needs", "image": "/subcategories/kitchen-&-dining-needs.webp"},
        {"name": "Classmate Notebook 180 pages", "description": "Single line long notebook for school", "unit": "1 pc", "stock": 100, "price": 55, "discount": 0, "cat": "Home & Office", "sub": "Stationery Needs", "image": "/subcategories/stationery-needs.webp"},

        # ─── Tea, Coffee & Health Drink ─────────────────────────────
        {"name": "Tata Tea Gold 500g", "description": "Premium blend of Assam tea leaves", "unit": "500 g", "stock": 100, "price": 260, "discount": 10, "cat": "Tea, Coffee & Health Drink", "sub": "Tea", "image": "/subcategories/tea.webp"},
        {"name": "Taj Mahal Tea 250g", "description": "Rich and aromatic brooke bond tea", "unit": "250 g", "stock": 90, "price": 165, "discount": 5, "cat": "Tea, Coffee & Health Drink", "sub": "Tea", "image": "/subcategories/tea.webp"},
        {"name": "Nescafe Classic Coffee 100g", "description": "Instant coffee with rich aroma", "unit": "100 g", "stock": 80, "price": 275, "discount": 10, "cat": "Tea, Coffee & Health Drink", "sub": "Coffee", "image": "/subcategories/coffee.jpg"},
        {"name": "Organic India Tulsi Green Tea 25 bags", "description": "Caffeine-free tulsi green tea", "unit": "25 bags", "stock": 70, "price": 175, "discount": 0, "cat": "Tea, Coffee & Health Drink", "sub": "Green & Flavoured Tea", "image": "/subcategories/green-&-flavoured-tea.webp"},

        # ─── Sweet Tooth ────────────────────────────────────────────
        {"name": "Cadbury Dairy Milk Silk 150g", "description": "Smooth and creamy milk chocolate", "unit": "150 g", "stock": 100, "price": 175, "discount": 0, "cat": "Sweet Tooth", "sub": "Chocolates", "image": "/subcategories/chocolates.png"},
        {"name": "KitKat Wafer Bar 37.3g", "description": "Crispy wafer covered in chocolate", "unit": "37.3 g", "stock": 180, "price": 30, "discount": 0, "cat": "Sweet Tooth", "sub": "Chocolates", "image": "/subcategories/chocolates.png"},
        {"name": "Amul Vanilla Ice Cream 750ml", "description": "Creamy real vanilla bean ice cream", "unit": "750 ml", "stock": 60, "price": 199, "discount": 10, "cat": "Sweet Tooth", "sub": "Ice Cream & Frozen Dessert", "image": "/subcategories/ice-cream-&-frozen-dessert.webp"},
        {"name": "Haldiram Rasgulla 1kg", "description": "Soft and spongy Bengali rasgulla", "unit": "1 kg", "stock": 50, "price": 220, "discount": 5, "cat": "Sweet Tooth", "sub": "Indian Sweets", "image": "/subcategories/indian-sweets.webp"},

        # ─── Baby Care ──────────────────────────────────────────────
        {"name": "Cerelac Wheat 300g", "description": "Stage 1 baby cereal with milk", "unit": "300 g", "stock": 80, "price": 225, "discount": 5, "cat": "Baby Care", "sub": "Baby Food", "image": "/subcategories/baby-food.webp"},
        {"name": "Nestle Lactogen 1 400g", "description": "Infant formula for 0-6 months", "unit": "400 g", "stock": 60, "price": 435, "discount": 0, "cat": "Baby Care", "sub": "Baby Food", "image": "/subcategories/baby-food.webp"},
        {"name": "Cerelac Rice 300g", "description": "Stage 1 rice-based baby cereal", "unit": "300 g", "stock": 70, "price": 225, "discount": 5, "cat": "Baby Care", "sub": "Baby Food", "image": "/subcategories/baby-food.webp"},

        # ─── Pet Care ───────────────────────────────────────────────
        {"name": "Pedigree Adult Chicken 3kg", "description": "Complete nutrition for adult dogs", "unit": "3 kg", "stock": 50, "price": 599, "discount": 10, "cat": "Pet Care", "sub": "Dog Needs", "image": "/subcategories/dog-needs.png"},
        {"name": "Drools Dog Treats 150g", "description": "Chicken-flavoured dog training treats", "unit": "150 g", "stock": 80, "price": 149, "discount": 0, "cat": "Pet Care", "sub": "Dog Needs", "image": "/subcategories/dog-needs.png"},
        {"name": "Whiskas Adult Cat Food Tuna 480g", "description": "Tuna-flavoured dry cat food", "unit": "480 g", "stock": 60, "price": 199, "discount": 5, "cat": "Pet Care", "sub": "Cat Needs", "image": "/subcategories/cat-needs.png"},

        # ─── Pharma & Wellness ──────────────────────────────────────
        {"name": "Crocin Advance 20 tablets", "description": "Paracetamol 500mg for pain and fever", "unit": "20 tabs", "stock": 150, "price": 28, "discount": 0, "cat": "Pharma & Wellness", "sub": "Everyday Medicines", "image": "/subcategories/everyday-medicines.webp"},
        {"name": "Dolo 650mg 15 tablets", "description": "Paracetamol for fever and headache", "unit": "15 tabs", "stock": 120, "price": 30, "discount": 0, "cat": "Pharma & Wellness", "sub": "Everyday Medicines", "image": "/subcategories/everyday-medicines.webp"},
        {"name": "Revital H Multivitamin 30 caps", "description": "Daily multivitamin with ginseng", "unit": "30 caps", "stock": 80, "price": 399, "discount": 10, "cat": "Pharma & Wellness", "sub": "Vitamins & Daily Nutrition", "image": "/subcategories/vitamins-&-daily-nutrition.webp"},
        {"name": "Vicks VapoRub 50ml", "description": "Topical cough suppressant and decongestant", "unit": "50 ml", "stock": 100, "price": 145, "discount": 5, "cat": "Pharma & Wellness", "sub": "Cough & Cold", "image": "/subcategories/cough-&-cold.webp"},

        # ─── Chicken, Meat & Fish ───────────────────────────────────
        {"name": "Licious Chicken Breast 500g", "description": "Fresh boneless chicken breast, antibiotic-free", "unit": "500 g", "stock": 60, "price": 250, "discount": 10, "cat": "Chicken, Meat & Fish", "sub": "Chicken", "image": "/subcategories/chicken.jpg"},
        {"name": "Licious Chicken Curry Cut 500g", "description": "Fresh curry-cut chicken with bone", "unit": "500 g", "stock": 80, "price": 199, "discount": 5, "cat": "Chicken, Meat & Fish", "sub": "Chicken", "image": "/subcategories/chicken.jpg"},
        {"name": "FreshToHome Rohu Fish 500g", "description": "Fresh river rohu fish steaks", "unit": "500 g", "stock": 50, "price": 199, "discount": 0, "cat": "Chicken, Meat & Fish", "sub": "Fish & Seafood", "image": "/subcategories/fish-&-seafood.jpg"},
        {"name": "Licious Chicken Sausages 200g", "description": "Ready-to-cook chicken sausages", "unit": "200 g", "stock": 70, "price": 179, "discount": 10, "cat": "Chicken, Meat & Fish", "sub": "Sausage, Salami & Ham", "image": "/subcategories/sausage-salami-&-ham.webp"},

        # ─── Organic & Healthy Living ───────────────────────────────
        {"name": "Happilo Almonds 200g", "description": "Premium California almonds, rich in Vitamin E", "unit": "200 g", "stock": 80, "price": 199, "discount": 10, "cat": "Organic & Healthy Living", "sub": "Dry Fruits", "image": "/subcategories/dry-fruits.webp"},
        {"name": "Nutraj Cashews 200g", "description": "Whole W320 grade cashew nuts", "unit": "200 g", "stock": 70, "price": 225, "discount": 5, "cat": "Organic & Healthy Living", "sub": "Dry Fruits", "image": "/subcategories/dry-fruits.webp"},
        {"name": "True Elements Muesli 400g", "description": "Crunchy muesli with fruits and nuts", "unit": "400 g", "stock": 60, "price": 299, "discount": 15, "cat": "Organic & Healthy Living", "sub": "Healthy Proteins", "image": "/subcategories/healthy-proteins.webp"},

        # ─── Paan Corner ────────────────────────────────────────────
        {"name": "Rajnigandha Pan Masala 10g", "description": "Premium silver-coated pan masala sachet", "unit": "10 g", "stock": 200, "price": 28, "discount": 0, "cat": "Paan Corner", "sub": "Paan", "image": "/subcategories/paan.webp"},
        {"name": "Pulse Candy Guava 50 pcs", "description": "Tangy guava-flavoured hard candy", "unit": "50 pcs", "stock": 150, "price": 100, "discount": 0, "cat": "Paan Corner", "sub": "Mouth Fresheners", "image": "/subcategories/mouth-fresheners.webp"},
        {"name": "Pass Pass Mouth Freshener 5.5g", "description": "Refreshing mint mouth freshener", "unit": "5.5 g", "stock": 180, "price": 10, "discount": 0, "cat": "Paan Corner", "sub": "Mouth Fresheners", "image": "/subcategories/mouth-fresheners.webp"},
    ]

    for p in products_data:
        product = Product(
            name=p["name"],
            description=p["description"],
            unit=p["unit"],
            stock=p["stock"],
            price=p["price"],
            discount=p["discount"],
            publish=True,
            image=[p["image"]],
        )
        product.category.append(categories[p["cat"]])
        product.subCategory.append(subcategories[p["sub"]])
        db.session.add(product)

    db.session.commit()
    total_subs = sum(len(v) for v in subcategories_map.values())
    print(f"Seeded {len(categories_data)} categories, {total_subs} subcategories, {len(products_data)} products.")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True, origins=["*"])

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_users()
        seed_data()
        print("MySQL tables created & seeded successfully")

    # Import and register blueprints
    from routes.user_routes import user_bp
    from routes.category_routes import category_bp
    from routes.subcategory_routes import subcategory_bp
    from routes.product_routes import product_bp
    from routes.cart_routes import cart_bp
    from routes.order_routes import order_bp
    from routes.upload_routes import upload_bp
    from routes.address_routes import address_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(subcategory_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(address_bp)

    # Serve uploaded images
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    @app.route("/uploads/<filename>")
    def serve_upload(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    @app.route("/api/placeholder/<text>")
    def placeholder_image(text):
        """Generate a colored SVG placeholder image with text."""
        import hashlib
        # Generate a consistent color from the text
        hash_val = int(hashlib.md5(text.encode()).hexdigest()[:6], 16)
        hue = hash_val % 360
        bg_color = f"hsl({hue}, 40%, 90%)"
        text_color = f"hsl({hue}, 60%, 35%)"
        display_text = text.replace("+", " ").replace("%20", " ")
        # Truncate long names
        if len(display_text) > 18:
            display_text = display_text[:16] + "..."

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
            <rect width="400" height="400" fill="{bg_color}" rx="20"/>
            <text x="200" y="190" font-family="Arial, sans-serif" font-size="28" font-weight="bold"
                  fill="{text_color}" text-anchor="middle" dominant-baseline="middle">{display_text}</text>
            <text x="200" y="230" font-family="Arial, sans-serif" font-size="14"
                  fill="{text_color}" opacity="0.6" text-anchor="middle">Cartify</text>
        </svg>'''

        from flask import Response
        return Response(svg, mimetype="image/svg+xml")

    @app.route("/")
    def index():
        return jsonify({"message": "Cartify Server is running"})

    return app


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8080))
    app = create_app()
    print(f"Cartify server running on http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
