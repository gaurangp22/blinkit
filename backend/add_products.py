"""Add many more products to every subcategory so the store looks full like Blinkit."""
import os, sys
os.environ["DATABASE_URL"] = os.environ.get("DATABASE_URL", "mysql+pymysql://root:cartify123@db:3306/cartify")
os.environ["SECRET_KEY"] = "cartify_secret_key_2025"

from app import create_app
from models import db, Category, SubCategory, Product

app = create_app()

# Products grouped by subcategory name
# Format: (name, description, unit, price, discount, image_file)
EXTRA_PRODUCTS = {
    # ── Fruits & Vegetables ──
    "Fresh Fruits": [
        ("Shimla Apple 4pc", "Premium Shimla apples, sweet and crunchy", "4 pcs", 120, 5, "/subcategories/fruits-&-vegetables.png"),
        ("Kela Robusta", "Fresh green bananas, great for cooking", "1 dozen", 45, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Pomegranate", "Ruby red pomegranate, loaded with antioxidants", "1 pc", 80, 10, "/subcategories/fruits-&-vegetables.png"),
        ("Papaya Medium", "Ripe papaya, rich in vitamins A and C", "1 pc", 55, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Kiwi Green 3pc", "Imported green kiwi, tangy and nutritious", "3 pcs", 110, 15, "/subcategories/fruits-&-vegetables.png"),
        ("Watermelon", "Sweet and juicy watermelon, perfect for summer", "1 pc", 60, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Mango Alphonso", "King of mangoes, sweet Alphonso from Ratnagiri", "1 kg", 350, 10, "/subcategories/fruits-&-vegetables.png"),
    ],
    "Fresh Vegetables": [
        ("Potato", "Farm fresh aloo, kitchen staple", "1 kg", 30, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Onion", "Red onions, essential for every Indian kitchen", "1 kg", 35, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Green Chilli 100g", "Spicy green chillies for that extra kick", "100 g", 10, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Coriander Leaves", "Fresh dhania patta for garnishing", "100 g", 12, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Spinach (Palak)", "Fresh organic spinach leaves", "250 g", 25, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Lady Finger (Bhindi)", "Tender lady finger, great for sabzi", "500 g", 40, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Brinjal (Baingan)", "Purple brinjal for bhartha and curries", "500 g", 30, 0, "/subcategories/fruits-&-vegetables.png"),
        ("Cauliflower", "Fresh white gobi, perfect for gobi manchurian", "1 pc", 35, 0, "/subcategories/fruits-&-vegetables.png"),
    ],
    # ── Dairy, Bread & Eggs ──
    "Milk": [
        ("Mother Dairy Full Cream 1L", "Rich and creamy full cream milk", "1 litre", 68, 0, "/subcategories/milk.webp"),
        ("Amul Gold Milk 500ml", "Standardized milk with added vitamins", "500 ml", 32, 0, "/subcategories/milk.webp"),
        ("Amul Taaza 500ml", "Fresh toned milk, great for daily use", "500 ml", 25, 0, "/subcategories/milk.webp"),
        ("Nestle a+ Toned Milk 1L", "Toned milk with goodness of calcium", "1 litre", 60, 5, "/subcategories/milk.webp"),
        ("Amul Buttermilk 200ml", "Spiced chaas, refreshing and light", "200 ml", 15, 0, "/subcategories/milk.webp"),
    ],
    "Bread & Pav": [
        ("Harvest Gold White Bread", "Soft white sandwich bread", "450 g", 40, 0, "/subcategories/bread-&-pav.webp"),
        ("Britannia Whole Wheat Bread", "100% whole wheat atta bread", "450 g", 50, 0, "/subcategories/bread-&-pav.webp"),
        ("Pav 6 pcs", "Soft ladi pav, perfect for vada pav", "6 pcs", 30, 0, "/subcategories/bread-&-pav.webp"),
        ("Amul Garlic Bread", "Ready to bake garlic bread with herbs", "200 g", 85, 10, "/subcategories/bread-&-pav.webp"),
        ("Britannia Milk Bread", "Enriched milk bread for sandwiches", "400 g", 45, 0, "/subcategories/bread-&-pav.webp"),
    ],
    "Eggs": [
        ("Farm Fresh Eggs 6pc", "Protein-packed fresh white eggs", "6 pcs", 48, 0, "/subcategories/eggs.webp"),
        ("Country Eggs 6pc", "Free-range brown eggs, desi style", "6 pcs", 72, 5, "/subcategories/eggs.webp"),
        ("Eggs 12pc Tray", "Value pack of 12 fresh eggs", "12 pcs", 90, 0, "/subcategories/eggs.webp"),
        ("Eggs 30pc Tray", "Bulk pack, great for families", "30 pcs", 210, 5, "/subcategories/eggs.webp"),
    ],
    "Cheese": [
        ("Amul Cheese Slices 10pc", "Processed cheese slices for burgers", "200 g", 125, 5, "/subcategories/cheese.webp"),
        ("Amul Cheese Block 200g", "Processed cheddar cheese block", "200 g", 105, 0, "/subcategories/cheese.webp"),
        ("Britannia Cheese Spread", "Creamy cheese spread for crackers", "180 g", 95, 10, "/subcategories/cheese.webp"),
        ("Go Mozzarella Cheese", "Shredded mozzarella for pizza", "200 g", 145, 5, "/subcategories/cheese.webp"),
    ],
    "Butter & More": [
        ("Amul Butter 100g", "Creamy salted butter, India's favorite", "100 g", 56, 0, "/subcategories/butter-&-more.webp"),
        ("Amul Butter 500g", "Value pack salted butter", "500 g", 270, 5, "/subcategories/butter-&-more.webp"),
        ("Britannia Cream Cheese", "Smooth cream cheese spread", "180 g", 99, 0, "/subcategories/butter-&-more.webp"),
    ],
    "Paneer & Tofu": [
        ("Amul Malai Paneer 200g", "Fresh soft malai paneer", "200 g", 90, 0, "/subcategories/paneer-&-tofu.webp"),
        ("Mother Dairy Paneer 200g", "Farm fresh cottage cheese", "200 g", 85, 5, "/subcategories/paneer-&-tofu.webp"),
        ("Tofu 200g", "Organic soy tofu for healthy cooking", "200 g", 65, 0, "/subcategories/paneer-&-tofu.webp"),
    ],
    # ── Snacks & Munchies ──
    "Chips & Crisps": [
        ("Lays Magic Masala 52g", "India's favorite masala chips", "52 g", 20, 0, "/subcategories/chips-&-crisps.webp"),
        ("Lays American Style Cream & Onion", "Creamy onion flavored potato chips", "52 g", 20, 0, "/subcategories/chips-&-crisps.webp"),
        ("Uncle Chipps Spicy Treat", "Classic Indian spicy chips", "55 g", 20, 0, "/subcategories/chips-&-crisps.webp"),
        ("Kurkure Masala Munch", "Crunchy namkeen snack", "90 g", 20, 0, "/subcategories/chips-&-crisps.webp"),
        ("Bingo Mad Angles", "Triangular corn chips with spicy taste", "72 g", 20, 0, "/subcategories/chips-&-crisps.webp"),
        ("Pringles Original 107g", "Stackable premium potato crisps", "107 g", 149, 10, "/subcategories/chips-&-crisps.webp"),
        ("Doritos Sweet Chilli", "Tortilla chips with sweet chilli flavor", "72 g", 40, 0, "/subcategories/chips-&-crisps.webp"),
    ],
    "Bhujia & Mixtures": [
        ("Haldiram Bhujia 200g", "Classic besan bhujia namkeen", "200 g", 55, 5, "/subcategories/bhujia-&-mixtures.webp"),
        ("Haldiram Moong Dal 200g", "Crispy fried moong dal", "200 g", 50, 0, "/subcategories/bhujia-&-mixtures.webp"),
        ("Haldiram Navrattan Mix", "Mixed namkeen with dry fruits", "200 g", 60, 10, "/subcategories/bhujia-&-mixtures.webp"),
        ("Bikaji Bhujia Sev", "Rajasthani style crispy sev", "200 g", 52, 0, "/subcategories/bhujia-&-mixtures.webp"),
        ("Haldiram Khatta Meetha", "Sweet and tangy namkeen mix", "200 g", 55, 0, "/subcategories/bhujia-&-mixtures.webp"),
    ],
    "Namkeen Snacks": [
        ("Haldiram Aloo Bhujia 400g", "Spicy potato sev namkeen", "400 g", 99, 10, "/subcategories/namkeen-snacks.webp"),
        ("Bikaji Bikaneri Bhujia", "Authentic Bikaner style bhujia", "200 g", 58, 0, "/subcategories/namkeen-snacks.webp"),
        ("Haldiram Mini Samosa", "Crispy bite-size samosas", "200 g", 65, 5, "/subcategories/namkeen-snacks.webp"),
    ],
    "Nachos": [
        ("Doritos Nachos Cheese 60g", "Cheese flavored tortilla chips", "60 g", 40, 0, "/subcategories/nachos.webp"),
        ("Too Yumm Multigrain Chips", "Healthy baked multigrain chips", "54 g", 30, 0, "/subcategories/nachos.webp"),
        ("Cornitos Nacho Crisps Cheese", "Mexican style nacho crisps", "60 g", 45, 10, "/subcategories/nachos.webp"),
    ],
    # ── Cold Drinks & Juices ──
    "Soft Drinks": [
        ("Coca Cola 2L", "Classic cola soft drink family pack", "2 litre", 90, 0, "/subcategories/soft-drinks.webp"),
        ("Pepsi 750ml", "Refreshing Pepsi cola", "750 ml", 38, 0, "/subcategories/soft-drinks.webp"),
        ("Sprite 2L", "Clear lemon-lime soda", "2 litre", 90, 0, "/subcategories/soft-drinks.webp"),
        ("Thumbs Up 750ml", "Strong fizzy cola", "750 ml", 38, 0, "/subcategories/soft-drinks.webp"),
        ("Fanta Orange 750ml", "Fruity orange soda", "750 ml", 38, 0, "/subcategories/soft-drinks.webp"),
        ("Mountain Dew 750ml", "Citrus blast energy drink", "750 ml", 38, 0, "/subcategories/soft-drinks.webp"),
        ("Coca Cola Zero 300ml", "Zero sugar zero calories cola", "300 ml", 35, 0, "/subcategories/soft-drinks.webp"),
    ],
    "Fruit Juices": [
        ("Real Mixed Fruit 1L", "Mixed fruit juice with no added sugar", "1 litre", 99, 10, "/subcategories/fruit-juices.webp"),
        ("Tropicana Apple 1L", "100% pure apple juice", "1 litre", 90, 5, "/subcategories/fruit-juices.webp"),
        ("Paper Boat Aam Panna", "Traditional raw mango drink", "200 ml", 30, 0, "/subcategories/fruit-juices.webp"),
        ("Real Pomegranate 1L", "Rich pomegranate juice", "1 litre", 110, 10, "/subcategories/fruit-juices.webp"),
        ("B Natural Mixed Fruit", "Goodness of 5 fruits", "1 litre", 85, 5, "/subcategories/fruit-juices.webp"),
    ],
    "Energy Drinks": [
        ("Red Bull 250ml", "Energy drink that gives you wings", "250 ml", 115, 0, "/subcategories/energy-drinks.webp"),
        ("Monster Energy 350ml", "Extreme energy boost drink", "350 ml", 125, 0, "/subcategories/energy-drinks.webp"),
        ("Sting Energy 250ml", "Affordable energy drink", "250 ml", 20, 0, "/subcategories/energy-drinks.webp"),
        ("Gatorade Sports Drink 500ml", "Electrolyte replenishment drink", "500 ml", 50, 0, "/subcategories/energy-drinks.webp"),
    ],
    "Coconut Water": [
        ("Paper Boat Coconut Water", "100% natural tender coconut water", "200 ml", 30, 0, "/subcategories/coconut-water.webp"),
        ("Raw Pressery Coconut Water", "Cold pressed coconut water", "200 ml", 45, 10, "/subcategories/coconut-water.webp"),
    ],
    # ── Breakfast & Instant Food ──
    "Noodles": [
        ("Maggi 2-Min Masala Noodles 4pk", "India's favorite instant noodles", "4 pcs", 56, 0, "/subcategories/noodles.webp"),
        ("Maggi 2-Min Noodles Single", "Quick masala noodles single pack", "1 pc", 14, 0, "/subcategories/noodles.webp"),
        ("Yippee Noodles Magic Masala", "Smooth round noodles", "70 g", 15, 0, "/subcategories/noodles.webp"),
        ("Top Ramen Curry Noodles", "Curry flavored instant noodles", "70 g", 15, 0, "/subcategories/noodles.webp"),
        ("Ching's Schezwan Noodles", "Spicy schezwan instant noodles", "60 g", 20, 0, "/subcategories/noodles.webp"),
        ("Maggi Hot Heads", "Extra spicy premium noodles", "71 g", 25, 0, "/subcategories/noodles.webp"),
    ],
    "Oats": [
        ("Quaker Oats 1kg", "Whole grain rolled oats", "1 kg", 180, 10, "/subcategories/oats.webp"),
        ("Saffola Masala Oats Classic", "Instant masala flavored oats", "39 g", 15, 0, "/subcategories/oats.webp"),
        ("Kellogg's Oats 500g", "Heart-healthy breakfast oats", "500 g", 120, 5, "/subcategories/oats.webp"),
    ],
    "Pasta": [
        ("Maggi Penne Pasta 400g", "Durum wheat penne pasta", "400 g", 55, 0, "/subcategories/pasta.webp"),
        ("Del Monte Fusilli Pasta", "Italian style fusilli pasta", "500 g", 85, 10, "/subcategories/pasta.webp"),
        ("Maggi Pasta Masala", "Instant cup pasta", "70 g", 25, 0, "/subcategories/pasta.webp"),
    ],
    "Ready to Cook & Eat": [
        ("MTR Ready to Eat Rajma", "Heat and eat rajma masala", "300 g", 85, 5, "/subcategories/ready-to-cook-&-eat.webp"),
        ("MTR Paneer Butter Masala", "Restaurant style paneer curry", "300 g", 95, 5, "/subcategories/ready-to-cook-&-eat.webp"),
        ("Haldiram Minute Khana Dal Makhani", "Ready to eat dal makhani", "300 g", 80, 0, "/subcategories/ready-to-cook-&-eat.webp"),
        ("ITC Aashirvaad Atta Noodles", "Healthy wheat noodles", "280 g", 40, 0, "/subcategories/ready-to-cook-&-eat.webp"),
    ],
    # ── Bakery & Biscuits ──
    "Cookies": [
        ("Britannia Good Day Cashew", "Buttery cashew cookies", "200 g", 40, 0, "/subcategories/cookies.webp"),
        ("Parle Hide & Seek Choco", "Chocolate chip cookies", "200 g", 42, 5, "/subcategories/cookies.webp"),
        ("Sunfeast Dark Fantasy Choco", "Premium dark chocolate cookies", "75 g", 30, 0, "/subcategories/cookies.webp"),
        ("Britannia NutriChoice Oats", "Healthy digestive oats cookies", "150 g", 40, 0, "/subcategories/cookies.webp"),
        ("Oreo Vanilla Cream 120g", "Chocolate cookies with vanilla filling", "120 g", 30, 0, "/subcategories/cookies.webp"),
        ("McVities Digestive 400g", "Whole wheat digestive biscuits", "400 g", 145, 10, "/subcategories/cookies.webp"),
    ],
    "Cream Biscuits": [
        ("Bourbon Cream Biscuits", "Chocolate cream filled biscuits", "150 g", 30, 0, "/subcategories/cream-biscuits.webp"),
        ("Parle 20-20 Butter Cookies", "Crispy butter cream cookies", "200 g", 35, 0, "/subcategories/cream-biscuits.webp"),
        ("Jim Jam Treats", "Jam filled cream biscuits", "150 g", 25, 0, "/subcategories/cream-biscuits.webp"),
    ],
    "Glucose & Marie": [
        ("Parle-G 250g", "India's original glucose biscuit", "250 g", 25, 0, "/subcategories/glucose-&-marie.webp"),
        ("Britannia Marie Gold 250g", "Light and crispy marie biscuit", "250 g", 35, 0, "/subcategories/glucose-&-marie.webp"),
        ("Parle-G Gold 100g", "Premium glucose biscuit", "100 g", 15, 0, "/subcategories/glucose-&-marie.webp"),
        ("Tiger Glucose 250g", "Britannia glucose biscuit", "250 g", 25, 0, "/subcategories/glucose-&-marie.webp"),
    ],
    "Cakes & Rolls": [
        ("Britannia Cake Chocolate", "Soft chocolate sponge cake", "75 g", 20, 0, "/subcategories/cakes-&-rolls.webp"),
        ("Parle Mango Bite Cake", "Mango flavored soft cake", "20 g", 10, 0, "/subcategories/cakes-&-rolls.webp"),
        ("Swiss Roll Chocolate", "Cream filled chocolate roll", "100 g", 35, 0, "/subcategories/cakes-&-rolls.webp"),
    ],
    # ── Atta, Rice & Dal ──
    "Atta & Flour": [
        ("Aashirvaad Atta 5kg", "Premium whole wheat atta", "5 kg", 285, 5, "/subcategories/atta-rice-&-dal.png"),
        ("Aashirvaad Multigrain Atta 5kg", "Multi-grain healthy atta", "5 kg", 330, 5, "/subcategories/atta-rice-&-dal.png"),
        ("Pillsbury Chakki Fresh Atta 5kg", "Stone ground fresh atta", "5 kg", 270, 0, "/subcategories/atta-rice-&-dal.png"),
        ("Besan (Gram Flour) 500g", "Fine gram flour for pakoras", "500 g", 65, 0, "/subcategories/atta-rice-&-dal.png"),
        ("Maida 1kg", "Refined all-purpose flour", "1 kg", 45, 0, "/subcategories/atta-rice-&-dal.png"),
        ("Sooji (Rava) 500g", "Semolina for upma and halwa", "500 g", 40, 0, "/subcategories/atta-rice-&-dal.png"),
    ],
    "Rice": [
        ("India Gate Basmati Rice 5kg", "Premium aged basmati rice", "5 kg", 495, 10, "/subcategories/atta-rice-&-dal.png"),
        ("Daawat Rozana Basmati 1kg", "Everyday basmati rice", "1 kg", 90, 5, "/subcategories/atta-rice-&-dal.png"),
        ("Kohinoor Super Value Basmati", "Long grain basmati rice", "1 kg", 115, 0, "/subcategories/atta-rice-&-dal.png"),
    ],
    "Dal & Pulses": [
        ("Toor Dal (Arhar) 1kg", "Premium split pigeon pea", "1 kg", 145, 5, "/subcategories/atta-rice-&-dal.png"),
        ("Moong Dal 1kg", "Split green gram dal", "1 kg", 135, 0, "/subcategories/atta-rice-&-dal.png"),
        ("Chana Dal 1kg", "Split bengal gram for dal", "1 kg", 95, 0, "/subcategories/atta-rice-&-dal.png"),
        ("Masoor Dal 1kg", "Red lentils for quick cooking", "1 kg", 100, 5, "/subcategories/atta-rice-&-dal.png"),
        ("Rajma 500g", "Red kidney beans for rajma masala", "500 g", 85, 0, "/subcategories/atta-rice-&-dal.png"),
        ("Chole (Kabuli Chana) 500g", "White chickpeas for chole", "500 g", 80, 0, "/subcategories/atta-rice-&-dal.png"),
    ],
    # ── Masala, Oil & More ──
    "Powdered Spices": [
        ("MDH Garam Masala 100g", "Aromatic blend of whole spices", "100 g", 72, 5, "/subcategories/powdered-spices.webp"),
        ("Everest Chilli Powder 100g", "Pure Kashmiri red chilli powder", "100 g", 42, 0, "/subcategories/powdered-spices.webp"),
        ("MDH Turmeric 100g", "Pure haldi powder", "100 g", 38, 0, "/subcategories/powdered-spices.webp"),
        ("Everest Coriander Powder 100g", "Ground dhania powder", "100 g", 35, 0, "/subcategories/powdered-spices.webp"),
        ("MDH Kitchen King Masala", "All-purpose curry masala", "100 g", 68, 5, "/subcategories/powdered-spices.webp"),
        ("Catch Cumin Powder 100g", "Ground jeera powder", "100 g", 55, 0, "/subcategories/powdered-spices.webp"),
    ],
    "Oil": [
        ("Fortune Sunflower Oil 1L", "Light refined sunflower oil", "1 litre", 135, 5, "/subcategories/oil.webp"),
        ("Saffola Gold Oil 1L", "Blended edible vegetable oil", "1 litre", 175, 10, "/subcategories/oil.webp"),
        ("Fortune Mustard Oil 1L", "Kachi ghani mustard oil", "1 litre", 165, 5, "/subcategories/oil.webp"),
        ("Figaro Olive Oil 200ml", "Extra virgin olive oil", "200 ml", 250, 10, "/subcategories/oil.webp"),
        ("Parachute Coconut Oil 500ml", "100% pure coconut oil", "500 ml", 115, 0, "/subcategories/oil.webp"),
    ],
    "Ghee & Vanaspati": [
        ("Amul Pure Ghee 500ml", "Pure cow ghee, rich aroma", "500 ml", 310, 5, "/subcategories/ghee-&-vanaspati.webp"),
        ("Patanjali Cow Ghee 500ml", "Desi cow ghee", "500 ml", 350, 0, "/subcategories/ghee-&-vanaspati.webp"),
        ("Mother Dairy Pure Ghee 1L", "Premium cow ghee", "1 litre", 620, 5, "/subcategories/ghee-&-vanaspati.webp"),
    ],
    "Salt, Sugar & Jaggery": [
        ("Tata Salt 1kg", "Iodized vacuum-evaporated salt", "1 kg", 28, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Sugar 1kg", "Refined white sugar", "1 kg", 48, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Organic Jaggery 500g", "Natural cane jaggery (Gur)", "500 g", 75, 10, "/subcategories/salt-sugar-&-jaggery.webp"),
        ("Rock Salt 1kg", "Sendha namak, pink rock salt", "1 kg", 50, 0, "/subcategories/salt-sugar-&-jaggery.webp"),
    ],
    # ── Sauces & Spreads ──
    "Tomato & Chilli Ketchup": [
        ("Kissan Tomato Ketchup 500g", "Rich tomato ketchup", "500 g", 105, 5, "/subcategories/tomato-&-chilli-ketchup.webp"),
        ("Maggi Hot & Sweet 500g", "Tomato chilli sauce", "500 g", 115, 5, "/subcategories/tomato-&-chilli-ketchup.webp"),
        ("Heinz Tomato Ketchup 450g", "Imported premium ketchup", "450 g", 165, 10, "/subcategories/tomato-&-chilli-ketchup.webp"),
        ("Del Monte Chilli Sauce", "Hot chilli garlic sauce", "190 g", 55, 0, "/subcategories/tomato-&-chilli-ketchup.webp"),
    ],
    "Jam & Spreads": [
        ("Kissan Mixed Fruit Jam 500g", "Classic mixed fruit jam", "500 g", 145, 10, "/subcategories/jam-&-spreads.webp"),
        ("Nutella Chocolate Spread 350g", "Hazelnut chocolate spread", "350 g", 399, 5, "/subcategories/jam-&-spreads.webp"),
        ("Sundrop Peanut Butter Creamy", "Smooth peanut butter", "462 g", 199, 10, "/subcategories/jam-&-spreads.webp"),
        ("Kissan Strawberry Jam 200g", "Sweet strawberry jam", "200 g", 75, 0, "/subcategories/jam-&-spreads.webp"),
    ],
    # ── Personal Care ──
    "Bathing Soaps": [
        ("Dove Cream Bar 100g", "Moisturizing beauty soap", "100 g", 55, 5, "/subcategories/bathing-soaps.webp"),
        ("Lux Soft Rose 150g", "Floral fragrance beauty soap", "150 g", 42, 0, "/subcategories/bathing-soaps.webp"),
        ("Dettol Original 125g", "Antibacterial protection soap", "125 g", 48, 0, "/subcategories/bathing-soaps.webp"),
        ("Pears Pure & Gentle 125g", "Glycerin transparent soap", "125 g", 65, 5, "/subcategories/bathing-soaps.webp"),
        ("Lifebuoy Total 10 125g", "Germ protection soap", "125 g", 35, 0, "/subcategories/bathing-soaps.webp"),
    ],
    "Shampoo & Conditioner": [
        ("Head & Shoulders 340ml", "Anti-dandruff shampoo", "340 ml", 185, 10, "/subcategories/shampoo-&-conditioner.webp"),
        ("Dove Daily Shine 340ml", "Nourishing shine shampoo", "340 ml", 215, 10, "/subcategories/shampoo-&-conditioner.webp"),
        ("Pantene Silky Smooth 340ml", "Silky smooth care shampoo", "340 ml", 199, 5, "/subcategories/shampoo-&-conditioner.webp"),
        ("Clinic Plus Strong 340ml", "Strong and long hair shampoo", "340 ml", 160, 0, "/subcategories/shampoo-&-conditioner.webp"),
        ("TRESemme Keratin 340ml", "Salon-smooth keratin shampoo", "340 ml", 295, 15, "/subcategories/shampoo-&-conditioner.webp"),
    ],
    "Face Wash & Scrub": [
        ("Himalaya Neem Face Wash", "Purifying neem face wash", "150 ml", 145, 10, "/subcategories/face-wash-&-scrub.webp"),
        ("Nivea Men Dark Spot Face Wash", "Skin brightening face wash", "100 ml", 175, 5, "/subcategories/face-wash-&-scrub.webp"),
        ("Clean & Clear Face Wash 80ml", "Oil-free daily face wash", "80 ml", 90, 0, "/subcategories/face-wash-&-scrub.webp"),
    ],
    "Handwash": [
        ("Dettol Original Handwash 200ml", "Germ-protection liquid handwash", "200 ml", 45, 0, "/subcategories/handwash.webp"),
        ("Lifebuoy Total 10 Handwash", "Complete protection handwash", "190 ml", 42, 0, "/subcategories/handwash.webp"),
        ("Santoor Handwash 200ml", "Gentle sandal handwash", "200 ml", 40, 0, "/subcategories/handwash.webp"),
    ],
    # ── Cleaning Essentials ──
    "Detergent Powder & Bars": [
        ("Surf Excel Easy Wash 1.5kg", "Effective stain remover detergent", "1.5 kg", 185, 10, "/subcategories/detergent-powder-&-bars.webp"),
        ("Tide Plus Extra Power 1kg", "Removes tough stains", "1 kg", 125, 5, "/subcategories/detergent-powder-&-bars.webp"),
        ("Ariel Matic Top Load 1kg", "For top load washing machines", "1 kg", 245, 10, "/subcategories/detergent-powder-&-bars.webp"),
        ("Rin Bar 250g", "Whitening detergent bar", "250 g", 22, 0, "/subcategories/detergent-powder-&-bars.webp"),
        ("Wheel Active Blue 1kg", "Affordable quality detergent", "1 kg", 65, 0, "/subcategories/detergent-powder-&-bars.webp"),
    ],
    "Floor Cleaners & More": [
        ("Lizol Citrus 500ml", "Disinfectant floor cleaner", "500 ml", 99, 5, "/subcategories/floor-cleaners-&-more.webp"),
        ("Harpic Power Plus 500ml", "Toilet cleaner disinfectant", "500 ml", 85, 0, "/subcategories/floor-cleaners-&-more.webp"),
        ("Domex Toilet Cleaner 500ml", "Thick toilet cleaning liquid", "500 ml", 78, 5, "/subcategories/floor-cleaners-&-more.webp"),
        ("Colin Glass Cleaner 500ml", "Streak-free glass cleaner", "500 ml", 95, 0, "/subcategories/floor-cleaners-&-more.webp"),
    ],
    "Dishwashing Bars": [
        ("Vim Dishwash Bar 250g", "Tough grease cleaning bar", "250 g", 25, 0, "/subcategories/dishwashing-bars.webp"),
        ("Vim Dishwash Gel 500ml", "Lemon fresh dishwash gel", "500 ml", 99, 10, "/subcategories/dishwashing-bars.webp"),
        ("Pril Dishwash Liquid 500ml", "Cuts through oil and grease", "500 ml", 110, 5, "/subcategories/dishwashing-bars.webp"),
    ],
    # ── Tea, Coffee & Health Drink ──
    "Tea": [
        ("Tata Tea Gold 500g", "Premium blend of Assam tea", "500 g", 270, 5, "/subcategories/tea.webp"),
        ("Red Label Tea 500g", "Natural care tea blend", "500 g", 250, 5, "/subcategories/tea.webp"),
        ("Taj Mahal Tea 250g", "Rich and aromatic tea", "250 g", 185, 0, "/subcategories/tea.webp"),
        ("Wagh Bakri Tea 500g", "Premium leaf tea", "500 g", 235, 5, "/subcategories/tea.webp"),
        ("Society Tea 500g", "Refreshing premium tea", "500 g", 245, 0, "/subcategories/tea.webp"),
    ],
    "Coffee": [
        ("Nescafe Classic 100g", "Instant coffee powder", "100 g", 275, 10, "/subcategories/coffee.jpg"),
        ("Bru Instant Coffee 100g", "Smooth instant coffee", "100 g", 235, 5, "/subcategories/coffee.jpg"),
        ("Continental Xtra Coffee 50g", "Strong instant coffee", "50 g", 115, 0, "/subcategories/coffee.jpg"),
        ("Nescafe Gold 100g", "Premium smooth coffee", "100 g", 495, 10, "/subcategories/coffee.jpg"),
    ],
    "Green & Flavoured Tea": [
        ("Lipton Green Tea 25bags", "Classic green tea bags", "25 bags", 145, 10, "/subcategories/green-&-flavoured-tea.webp"),
        ("Organic India Tulsi Tea 25bags", "Holy basil green tea", "25 bags", 175, 5, "/subcategories/green-&-flavoured-tea.webp"),
        ("Tetley Green Tea Lemon 25bags", "Refreshing lemon green tea", "25 bags", 155, 5, "/subcategories/green-&-flavoured-tea.webp"),
    ],
    # ── Sweet Tooth ──
    "Chocolates": [
        ("Dairy Milk Silk 150g", "Smooth and creamy milk chocolate", "150 g", 160, 0, "/subcategories/chocolates.png"),
        ("5 Star 40g", "Caramel and nougat chocolate bar", "40 g", 30, 0, "/subcategories/chocolates.png"),
        ("KitKat 4 Finger", "Crispy wafer chocolate", "37 g", 30, 0, "/subcategories/chocolates.png"),
        ("Ferrero Rocher 3pc", "Premium hazelnut chocolate", "3 pcs", 150, 0, "/subcategories/chocolates.png"),
        ("Munch 23g", "Crunchy coated wafer bar", "23 g", 10, 0, "/subcategories/chocolates.png"),
        ("Perk 22g", "Light wafer chocolate", "22 g", 10, 0, "/subcategories/chocolates.png"),
        ("Dairy Milk Fruit & Nut", "Milk chocolate with raisins and almonds", "80 g", 95, 5, "/subcategories/chocolates.png"),
    ],
    "Candies & Gum": [
        ("Mentos Roll", "Fresh mint flavored candy roll", "1 roll", 10, 0, "/subcategories/candies-&-gum.webp"),
        ("Halls Mint 9pc", "Cool mint cough drops", "1 strip", 15, 0, "/subcategories/candies-&-gum.webp"),
        ("Center Fresh Spearmint", "Fresh breath chewing gum", "1 pack", 10, 0, "/subcategories/candies-&-gum.webp"),
        ("Pulse Candy Guava", "Tangy kaccha aam candy", "1 pack", 50, 0, "/subcategories/candies-&-gum.webp"),
    ],
    "Ice Cream & Frozen Dessert": [
        ("Amul Vanilla Tub 1L", "Classic vanilla ice cream", "1 litre", 260, 10, "/subcategories/ice-cream-&-frozen-dessert.webp"),
        ("Cornetto Butterscotch", "Crunchy cone ice cream", "1 pc", 40, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
        ("Magnum Classic 80ml", "Premium dark chocolate ice cream", "80 ml", 99, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
        ("Amul Chocobar", "Chocolate coated ice cream bar", "1 pc", 25, 0, "/subcategories/ice-cream-&-frozen-dessert.webp"),
    ],
    # ── Home & Office ──
    "Kitchen & Dining Needs": [
        ("Aluminium Foil 9m", "Kitchen aluminium foil roll", "9 m", 85, 0, "/subcategories/kitchen-&-dining-needs.webp"),
        ("Cling Wrap 30m", "Food wrapping cling film", "30 m", 95, 5, "/subcategories/kitchen-&-dining-needs.webp"),
        ("Kitchen Towel 2 Rolls", "Absorbent paper towel rolls", "2 rolls", 120, 10, "/subcategories/kitchen-&-dining-needs.webp"),
        ("Scotch-Brite Scrub Pad 3pc", "Heavy duty scrub pads", "3 pcs", 45, 0, "/subcategories/kitchen-&-dining-needs.webp"),
    ],
    "Stationery Needs": [
        ("Cello Pen Pack 5pc", "Blue ball point pen pack", "5 pcs", 25, 0, "/subcategories/stationery-needs.webp"),
        ("Fevicol 50g", "Multi-purpose white adhesive", "50 g", 22, 0, "/subcategories/stationery-needs.webp"),
        ("Scotch Tape", "Transparent adhesive tape", "1 roll", 20, 0, "/subcategories/stationery-needs.webp"),
    ],
    # ── Baby Care ──
    "Baby Food": [
        ("Cerelac Wheat Apple 300g", "Stage 2 baby cereal", "300 g", 265, 5, "/subcategories/baby-food.webp"),
        ("Cerelac Rice 300g", "Stage 1 baby cereal", "300 g", 255, 5, "/subcategories/baby-food.webp"),
        ("Nestle Lactogen 1 400g", "Infant milk formula", "400 g", 450, 0, "/subcategories/baby-food.webp"),
    ],
    "Diapers & More": [
        ("Pampers Small 22pc", "Soft baby diapers S size", "22 pcs", 299, 10, "/subcategories/dispers-&-more.webp"),
        ("MamyPoko Pants M 38pc", "Pant style diaper medium", "38 pcs", 599, 15, "/subcategories/dispers-&-more.webp"),
        ("Huggies Wonder Pants L 32pc", "Large size pant diaper", "32 pcs", 549, 10, "/subcategories/dispers-&-more.webp"),
    ],
    "Baby Wipes": [
        ("Johnson's Baby Wipes 80pc", "Gentle cleansing baby wipes", "80 pcs", 195, 10, "/subcategories/baby-wipes.webp"),
        ("Pampers Baby Wipes 72pc", "Soft moist baby wipes", "72 pcs", 185, 5, "/subcategories/baby-wipes.webp"),
    ],
    # ── Pet Care ──
    "Dog Needs": [
        ("Pedigree Adult Chicken 1.2kg", "Chicken & vegetable dry food", "1.2 kg", 245, 5, "/subcategories/dog-needs.png"),
        ("Pedigree Puppy Milk 1.2kg", "Puppy milk & cereal food", "1.2 kg", 265, 5, "/subcategories/dog-needs.png"),
        ("Drools Chicken & Egg 3kg", "Dry dog food with real chicken", "3 kg", 499, 10, "/subcategories/dog-needs.png"),
    ],
    "Cat Needs": [
        ("Whiskas Adult Tuna 480g", "Tuna flavored cat food", "480 g", 165, 5, "/subcategories/cat-needs.png"),
        ("Me-O Tuna Cat Food 1.2kg", "Ocean fish adult cat food", "1.2 kg", 285, 10, "/subcategories/cat-needs.png"),
    ],
    # ── Pharma & Wellness ──
    "Everyday Medicines": [
        ("Crocin Advance 15tab", "Pain and fever relief tablets", "15 tabs", 30, 0, "/subcategories/everyday-medicines.webp"),
        ("Vicks VapoRub 25ml", "Cold and cough relief balm", "25 ml", 62, 0, "/subcategories/everyday-medicines.webp"),
        ("Moov Pain Relief 50g", "Fast pain relief cream", "50 g", 85, 5, "/subcategories/everyday-medicines.webp"),
        ("Dabur Honitus Cough Syrup", "Ayurvedic cough syrup", "100 ml", 72, 0, "/subcategories/everyday-medicines.webp"),
        ("Band-Aid Flexible 10pc", "Adhesive bandage strips", "10 pcs", 35, 0, "/subcategories/everyday-medicines.webp"),
    ],
    "Vitamins & Daily Nutrition": [
        ("Revital H Men 30cap", "Daily health supplement", "30 caps", 355, 10, "/subcategories/vitamins-&-daily-nutrition.webp"),
        ("Limcee Vitamin C 15tab", "Chewable vitamin C tablets", "15 tabs", 22, 0, "/subcategories/vitamins-&-daily-nutrition.webp"),
        ("Celin 500mg Vitamin C 15tab", "Vitamin C supplement", "15 tabs", 28, 0, "/subcategories/vitamins-&-daily-nutrition.webp"),
    ],
    # ── Chicken, Meat & Fish ──
    "Chicken": [
        ("Chicken Breast Boneless 500g", "Fresh boneless chicken breast", "500 g", 220, 5, "/subcategories/chicken.jpg"),
        ("Chicken Curry Cut 500g", "Fresh curry cut with bone", "500 g", 170, 0, "/subcategories/chicken.jpg"),
        ("Chicken Drumstick 500g", "Juicy chicken legs", "500 g", 180, 5, "/subcategories/chicken.jpg"),
        ("Chicken Keema 500g", "Minced chicken for kebabs", "500 g", 235, 0, "/subcategories/chicken.jpg"),
    ],
    "Fish & Seafood": [
        ("Rohu Fish Curry Cut 500g", "Fresh river fish pieces", "500 g", 210, 5, "/subcategories/fish-&-seafood.jpg"),
        ("Prawns Medium 250g", "Fresh medium-size prawns", "250 g", 295, 10, "/subcategories/fish-&-seafood.jpg"),
        ("Surmai Steaks 250g", "King mackerel steaks", "250 g", 320, 5, "/subcategories/fish-&-seafood.jpg"),
    ],
    # ── Organic & Healthy Living ──
    "Dry Fruits": [
        ("Almonds (Badam) 200g", "Premium California almonds", "200 g", 235, 10, "/subcategories/dry-fruits.webp"),
        ("Cashew (Kaju) 200g", "Whole white cashew nuts", "200 g", 265, 10, "/subcategories/dry-fruits.webp"),
        ("Raisins (Kishmish) 200g", "Golden seedless raisins", "200 g", 95, 5, "/subcategories/dry-fruits.webp"),
        ("Walnuts (Akhrot) 200g", "Whole walnut kernels", "200 g", 285, 10, "/subcategories/dry-fruits.webp"),
        ("Mixed Dry Fruits 200g", "Premium assorted mix", "200 g", 275, 15, "/subcategories/dry-fruits.webp"),
    ],
    "Healthy Proteins": [
        ("Peanut Butter Creamy 400g", "High protein peanut butter", "400 g", 199, 10, "/subcategories/healthy-proteins.webp"),
        ("Flax Seeds 200g", "Organic omega-3 rich flax seeds", "200 g", 85, 0, "/subcategories/healthy-proteins.webp"),
        ("Chia Seeds 200g", "Superfood chia seeds", "200 g", 175, 15, "/subcategories/healthy-proteins.webp"),
    ],
    # ── Paan Corner ──
    "Paan": [
        ("Rajnigandha Silver Pearls", "Premium silver coated pearls", "1 pouch", 35, 0, "/subcategories/paan.webp"),
        ("Vimal Pan Masala", "Classic pan masala sachet", "1 pouch", 15, 0, "/subcategories/paan.webp"),
    ],
    "Mouth Fresheners": [
        ("Pass Pass Pulse Candy", "Tangy hard-boiled candy", "50 g", 20, 0, "/subcategories/mouth-fresheners.webp"),
        ("Hajmola Regular 120tab", "Tasty digestive tablets", "120 tabs", 45, 0, "/subcategories/mouth-fresheners.webp"),
        ("Chingles Mint Gum", "Refreshing mint chewing gum", "1 pack", 10, 0, "/subcategories/mouth-fresheners.webp"),
    ],
}

with app.app_context():
    added = 0
    skipped_subs = []
    for sub_name, products in EXTRA_PRODUCTS.items():
        sub = SubCategory.query.filter_by(name=sub_name).first()
        if not sub:
            # Try to create the subcategory by matching category
            skipped_subs.append(sub_name)
            continue

        cat = sub.category[0] if sub.category else None

        for name, desc, unit, price, discount, image in products:
            # Skip if product already exists
            if Product.query.filter_by(name=name).first():
                continue

            product = Product(
                name=name,
                description=desc,
                unit=unit,
                stock=100 + (hash(name) % 100),
                price=price,
                discount=discount,
                publish=True,
                image=[image],
            )
            if cat:
                product.category.append(cat)
            product.subCategory.append(sub)
            db.session.add(product)
            added += 1

    db.session.commit()

    # Print summary
    total = Product.query.count()
    print(f"\nAdded {added} new products. Total products: {total}")
    if skipped_subs:
        print(f"Skipped subcategories (not found): {skipped_subs}")

    # Print counts per category
    cats = Category.query.all()
    for c in cats:
        count = Product.query.filter(Product.category.any(id=c.id)).count()
        print(f"  {c.name}: {count} products")
