from app import app, db
from models import User
import bcrypt

with app.app_context():
    # 1. Create client
    client_email = "client@cartify.com"
    if not User.query.filter_by(email=client_email).first():
        hashed = bcrypt.hashpw("Password123".encode(), bcrypt.gensalt()).decode()
        u = User(name="Client User", email=client_email, password=hashed, role="USER")
        db.session.add(u)
    
    # 2. Create admin
    admin_email = "admin@cartify.com"
    if not User.query.filter_by(email=admin_email).first():
        hashed = bcrypt.hashpw("Password123".encode(), bcrypt.gensalt()).decode()
        u = User(name="Admin User", email=admin_email, password=hashed, role="ADMIN")
        db.session.add(u)
    
    db.session.commit()
    print("Users created: client@cartify.com (Password123), admin@cartify.com (Password123)")
