"""Add more products for subcategories that were skipped or low."""
import os
os.environ["DATABASE_URL"] = os.environ.get("DATABASE_URL", "mysql+pymysql://root:cartify123@db:3306/cartify")
os.environ["SECRET_KEY"] = "cartify_secret_key_2025"

from app import create_app
from models import db, Category, SubCategory, Product

app = create_app()

# Using EXACT subcategory names from the database
EXTRA = {
    "Curd & Yogurt": [
        ("Amul Masti Dahi 400g", "Thick set curd, creamy and fresh", "400 g", 35, 0, "/subcategories/curd-&-yogurt.jpg"),
        ("Mother Dairy Dahi 400g", "Fresh probiotic curd", "400 g", 32, 0, "/subcategories/curd-&-yogurt.jpg"),
        ("Epigamia Greek Yogurt Strawberry", "High protein Greek yogurt", "90 g", 45, 10, "/subcategories/curd-&-yogurt.jpg"),
        ("Amul Lassi Mango 200ml", "Sweet mango flavored lassi", "200 ml", 25, 0, "/subcategories/curd-&-yogurt.jpg"),
    ],
    "Indian Chutney & Pickle": [
        ("Mothers Recipe Mango Pickle 300g", "Traditional aam ka achaar", "300 g", 85, 5, "/subcategories/indian-chutney-&-pickle.webp"),
        ("Kissan Jam Mixed Fruit 200g", "Classic mixed fruit preserve", "200 g", 75, 0, "/subcategories/indian-chutney-&-pickle.webp"),
        ("Priya Lime Pickle 300g", "Tangy lemon pickle", "300 g", 80, 0, "/subcategories/indian-chutney-&-pickle.webp"),
        ("MTR Coconut Chutney Powder", "Instant chutney mix", "100 g", 45, 0, "/subcategories/indian-chutney-&-pickle.webp"),
    ],
    "Face Care": [
        ("Himalaya Neem Face Wash 150ml", "Purifying neem face cleanser", "150 ml", 145, 10, "/subcategories/face-care.png"),
        ("Nivea Men Dark Spot Face Wash", "Brightening face wash for men", "100 ml", 175, 5, "/subcategories/face-care.png"),
        ("Clean & Clear Face Wash 80ml", "Oil-free daily cleanser", "80 ml", 90, 0, "/subcategories/face-care.png"),
        ("Pond's White Beauty Cream 50g", "Spot-less fairness cream", "50 g", 150, 10, "/subcategories/face-care.png"),
        ("Vaseline Body Lotion 200ml", "Deep moisture body lotion", "200 ml", 165, 5, "/subcategories/face-care.png"),
    ],
    "Ice Cream & Frozen Dessert": [
        ("Amul Vanilla Cup 100ml", "Classic vanilla ice cream cup", "100 ml", 30, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
        ("Cornetto Butterscotch Cone", "Crunchy cone with butterscotch", "1 pc", 40, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
        ("Magnum Classic Bar", "Premium dark chocolate ice cream", "80 ml", 99, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
        ("Amul Chocobar Ice Cream", "Chocolate coated ice cream bar", "1 pc", 25, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
        ("Kwality Wall's Feast", "Orange ice cream bar", "1 pc", 15, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
    ],
    "Indian Sweets": [
        ("Haldiram Gulab Jamun 500g", "Soft milk-solid dumplings in syrup", "500 g", 140, 5, "/subcategories/indian-sweets.webp"),
        ("Haldiram Rasgulla Tin 1kg", "Bengali style spongy rasgulla", "1 kg", 175, 10, "/subcategories/indian-sweets.webp"),
        ("Bikaji Soan Papdi 250g", "Flaky layered Indian sweet", "250 g", 85, 0, "/subcategories/indian-sweets.webp"),
        ("MTR Badam Drink Mix 200g", "Instant almond milk mix", "200 g", 115, 5, "/subcategories/indian-sweets.webp"),
    ],
    "Baby Food": [
        ("Cerelac Wheat Apple 300g", "Stage 2 baby cereal with apple", "300 g", 265, 5, "/subcategories/baby-food.webp"),
        ("Cerelac Rice Vegetables 300g", "Stage 1 baby cereal", "300 g", 255, 5, "/subcategories/baby-food.webp"),
        ("Nestle Lactogen 1 400g", "Infant milk formula stage 1", "400 g", 450, 0, "/subcategories/baby-food.webp"),
        ("Enfagrow A+ Stage 3 400g", "Toddler nutritional milk drink", "400 g", 530, 10, "/subcategories/baby-food.webp"),
        ("Cerelac Multigrain Dal Veg", "Multi-grain baby food", "300 g", 270, 5, "/subcategories/baby-food.webp"),
    ],
    "Appliances": [
        ("LED Bulb 9W Philips", "Energy saving LED bulb", "1 pc", 99, 10, "/subcategories/appliances.webp"),
        ("Extension Board 4 Socket", "Surge protected power strip", "1 pc", 245, 5, "/subcategories/appliances.webp"),
        ("Mobile Charger USB-C", "Fast charging adapter", "1 pc", 299, 15, "/subcategories/appliances.webp"),
        ("Power Bank 10000mAh", "Portable charger for phones", "1 pc", 699, 10, "/subcategories/appliances.webp"),
    ],
    "Sausage, Salami & Ham": [
        ("Chicken Sausages 250g", "Smoked chicken sausages", "250 g", 160, 5, "/subcategories/sausage-salami-&-ham.webp"),
        ("Chicken Salami 200g", "Sliced chicken salami", "200 g", 140, 0, "/subcategories/sausage-salami-&-ham.webp"),
        ("Pork Frankfurter 250g", "Classic pork franks", "250 g", 195, 10, "/subcategories/sausage-salami-&-ham.webp"),
    ],
    "Cough & Cold": [
        ("Vicks Action 500 10tab", "Cold and flu relief tablets", "10 tabs", 42, 0, "/subcategories/cough-&-cold.webp"),
        ("Strepsils 8pc", "Sore throat lozenges", "8 pcs", 35, 0, "/subcategories/cough-&-cold.webp"),
        ("Dabur Honitus Syrup 100ml", "Ayurvedic honey cough syrup", "100 ml", 72, 5, "/subcategories/cough-&-cold.webp"),
        ("Otrivin Nasal Spray 10ml", "Blocked nose relief spray", "10 ml", 88, 0, "/subcategories/cough-&-cold.webp"),
    ],
    "Dry Fruits": [
        ("Almonds California 200g", "Premium California almonds", "200 g", 235, 10, "/subcategories/dry-fruits.webp"),
        ("Cashew Whole 200g", "White whole cashew nuts", "200 g", 265, 10, "/subcategories/dry-fruits.webp"),
        ("Raisins Kishmish 200g", "Golden seedless raisins", "200 g", 95, 5, "/subcategories/dry-fruits.webp"),
        ("Walnuts Akhrot 200g", "Premium walnut kernels", "200 g", 285, 10, "/subcategories/dry-fruits.webp"),
        ("Mixed Dry Fruits Pack", "Assorted premium dry fruits", "200 g", 275, 15, "/subcategories/dry-fruits.webp"),
        ("Pista Salted 200g", "Roasted salted pistachios", "200 g", 295, 10, "/subcategories/dry-fruits.webp"),
        ("Dates Medjool 250g", "Imported medjool dates", "250 g", 320, 5, "/subcategories/dry-fruits.webp"),
    ],
    "Healthy Proteins": [
        ("Peanut Butter Creamy 400g", "High protein smooth peanut butter", "400 g", 199, 10, "/subcategories/healthy-proteins.webp"),
        ("Flax Seeds 200g", "Omega-3 rich flax seeds", "200 g", 85, 0, "/subcategories/healthy-proteins.webp"),
        ("Chia Seeds 200g", "Superfood chia seeds", "200 g", 175, 15, "/subcategories/healthy-proteins.webp"),
        ("Quinoa 500g", "Organic white quinoa grain", "500 g", 245, 10, "/subcategories/healthy-proteins.webp"),
        ("Protein Bar Chocolate 60g", "High protein snack bar", "60 g", 99, 0, "/subcategories/healthy-proteins.webp"),
    ],
    "Salt, Sugar & Jaggery": [
        ("Tata Salt 1kg", "Vacuum evaporated iodized salt", "1 kg", 28, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Sugar 1kg", "Refined white crystal sugar", "1 kg", 48, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Organic Jaggery Powder 500g", "Natural cane gur powder", "500 g", 75, 10, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Rock Salt Sendha 1kg", "Pink Himalayan rock salt", "1 kg", 50, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Brown Sugar 500g", "Unrefined brown sugar", "500 g", 55, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Mishri Crystal 250g", "Rock candy sugar crystals", "250 g", 65, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
    ],
    "Paan": [
        ("Rajnigandha Silver 10g", "Premium silver coated pan masala", "10 g", 35, 0, "/subcategories/paan.webp"),
        ("Pan Bahar Sachet", "Classic pan masala", "1 pouch", 12, 0, "/subcategories/paan.webp"),
        ("Baba 120 Elaichi", "Elaichi flavored pan masala", "1 pouch", 20, 0, "/subcategories/paan.webp"),
    ],
    "Mouth Fresheners": [
        ("Hajmola Regular Bottle", "Tasty digestive tablets", "120 tabs", 45, 0, "/subcategories/mouth-fresheners.webp"),
        ("Pass Pass Candy 50g", "Tangy hard candy", "50 g", 20, 0, "/subcategories/mouth-fresheners.webp"),
        ("Orbit Spearmint Gum", "Sugar-free mint gum", "1 pack", 10, 0, "/subcategories/mouth-fresheners.webp"),
        ("Chingles Watermelon Gum", "Fruity chewing gum", "1 pack", 10, 0, "/subcategories/mouth-fresheners.webp"),
        ("Tic Tac Mint 7.7g", "Tiny mint breath freshener", "7.7 g", 20, 0, "/subcategories/mouth-fresheners.webp"),
    ],
    "Dog Needs": [
        ("Pedigree Adult Chicken 3kg", "Complete chicken dry dog food", "3 kg", 570, 10, "/subcategories/dog-needs.png"),
        ("Pedigree Puppy Food 1.2kg", "Starter puppy nutrition", "1.2 kg", 265, 5, "/subcategories/dog-needs.png"),
        ("Drools Chicken Egg 3kg", "Real chicken adult dog food", "3 kg", 499, 10, "/subcategories/dog-needs.png"),
        ("Pedigree Dentastix 7pc", "Dog dental care treats", "7 pcs", 125, 0, "/subcategories/dog-needs.png"),
        ("Dog Chew Bone Small", "Natural rawhide chew bone", "1 pc", 45, 0, "/subcategories/dog-needs.png"),
    ],
    "Cat Needs": [
        ("Whiskas Adult Tuna 480g", "Tuna flavor dry cat food", "480 g", 165, 5, "/subcategories/cat-needs.png"),
        ("Me-O Tuna 1.2kg", "Ocean fish adult cat food", "1.2 kg", 285, 10, "/subcategories/cat-needs.png"),
        ("Whiskas Kitten Food 450g", "Junior cat dry food", "450 g", 155, 5, "/subcategories/cat-needs.png"),
        ("Cat Litter Sand 5kg", "Clumping cat litter", "5 kg", 350, 10, "/subcategories/cat-needs.png"),
    ],
    "Chicken": [
        ("Chicken Breast Boneless 500g", "Fresh skinless breast pieces", "500 g", 220, 5, "/subcategories/chicken.jpg"),
        ("Chicken Curry Cut 1kg", "Bone-in curry pieces", "1 kg", 310, 5, "/subcategories/chicken.jpg"),
        ("Chicken Drumstick 500g", "Juicy whole legs", "500 g", 180, 0, "/subcategories/chicken.jpg"),
        ("Chicken Keema 500g", "Minced chicken for kebabs", "500 g", 235, 5, "/subcategories/chicken.jpg"),
        ("Chicken Wings 500g", "Party-style chicken wings", "500 g", 175, 0, "/subcategories/chicken.jpg"),
        ("Chicken Lollipop 250g", "Marinated ready-to-fry lollipops", "250 g", 195, 10, "/subcategories/chicken.jpg"),
    ],
    "Fish & Seafood": [
        ("Rohu Fish Curry Cut 500g", "Fresh river fish pieces", "500 g", 210, 5, "/subcategories/fish-&-seafood.jpg"),
        ("Prawns Medium 250g", "Cleaned medium prawns", "250 g", 295, 10, "/subcategories/fish-&-seafood.jpg"),
        ("Surmai Steaks 250g", "King mackerel fresh steaks", "250 g", 320, 5, "/subcategories/fish-&-seafood.jpg"),
        ("Pomfret Medium 1pc", "Fresh whole pomfret fish", "1 pc", 280, 0, "/subcategories/fish-&-seafood.jpg"),
        ("Basa Fillet 500g", "Boneless basa fish fillets", "500 g", 265, 10, "/subcategories/fish-&-seafood.jpg"),
    ],
}

with app.app_context():
    added = 0
    for sub_name, products in EXTRA.items():
        sub = SubCategory.query.filter_by(name=sub_name).first()
        if not sub:
            print(f"NOT FOUND: {sub_name}")
            continue
        cat = sub.category[0] if sub.category else None
        for name, desc, unit, price, discount, image in products:
            if Product.query.filter_by(name=name).first():
                continue
            p = Product(name=name, description=desc, unit=unit, stock=100+(hash(name)%100), price=price, discount=discount, publish=True, image=[image])
            if cat:
                p.category.append(cat)
            p.subCategory.append(sub)
            db.session.add(p)
            added += 1
    db.session.commit()

    total = Product.query.count()
    print(f"\nAdded {added} new. Total: {total}")
    for c in Category.query.all():
        cnt = Product.query.filter(Product.category.any(id=c.id)).count()
        print(f"  {c.name}: {cnt}")
