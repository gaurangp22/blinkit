from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


# ── Junction Tables ──────────────────────────────────────────────

subcategory_categories = db.Table(
    "subcategory_categories",
    db.Column("subcategory_id", db.Integer, db.ForeignKey("sub_category.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"), primary_key=True),
)

product_categories = db.Table(
    "product_categories",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"), primary_key=True),
)

product_subcategories = db.Table(
    "product_subcategories",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("subcategory_id", db.Integer, db.ForeignKey("sub_category.id"), primary_key=True),
)


# ── User ─────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(20), default="")
    avatar = db.Column(db.String(500), default="")
    status = db.Column(db.String(20), default="Active")
    role = db.Column(db.String(20), default="USER")
    last_login_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    addresses = db.relationship("Address", backref="user", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "email": self.email,
            "avatar": self.avatar or "",
            "mobile": self.mobile or "",
            "verify_email": True,
            "last_login_date": self.last_login_date.isoformat() if self.last_login_date else "",
            "status": self.status,
            "role": self.role,
            "createdAt": self.created_at.isoformat() if self.created_at else "",
            "updatedAt": self.updated_at.isoformat() if self.updated_at else "",
        }


# ── Category ─────────────────────────────────────────────────────

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(500), default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "image": self.image or "",
            "createdAt": self.created_at.isoformat() if self.created_at else "",
            "updatedAt": self.updated_at.isoformat() if self.updated_at else "",
        }


# ── SubCategory ──────────────────────────────────────────────────

class SubCategory(db.Model):
    __tablename__ = "sub_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(500), default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category = db.relationship("Category", secondary=subcategory_categories, backref="subcategories", lazy=True)

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "image": self.image or "",
            "category": [c.to_dict() for c in self.category],
            "createdAt": self.created_at.isoformat() if self.created_at else "",
            "updatedAt": self.updated_at.isoformat() if self.updated_at else "",
        }


# ── Product ──────────────────────────────────────────────────────

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.JSON, default=list)
    description = db.Column(db.Text, default="")
    unit = db.Column(db.String(100), default="")
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    more_details = db.Column(db.JSON, default=dict)
    publish = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category = db.relationship("Category", secondary=product_categories, backref="products", lazy=True)
    subCategory = db.relationship("SubCategory", secondary=product_subcategories, backref="products", lazy=True)

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "image": self.image or [],
            "category": [c.to_dict() for c in self.category],
            "subCategory": [s.to_dict() for s in self.subCategory],
            "description": self.description or "",
            "unit": self.unit or "",
            "stock": self.stock,
            "price": self.price,
            "discount": self.discount,
            "more_details": self.more_details or {},
            "publish": self.publish,
            "createdAt": self.created_at.isoformat() if self.created_at else "",
            "updatedAt": self.updated_at.isoformat() if self.updated_at else "",
        }


# ── Cart (per-item, linked to user & product) ───────────────────

class CartProduct(db.Model):
    __tablename__ = "cart_product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    product = db.relationship("Product", backref="cart_items", lazy=True)

    def to_dict(self):
        return {
            "_id": self.id,
            "productId": self.product.to_dict() if self.product else None,
            "userId": self.user_id,
            "quantity": self.quantity,
            "createdAt": self.created_at.isoformat() if self.created_at else "",
            "updatedAt": self.updated_at.isoformat() if self.updated_at else "",
        }


# ── Address (User Delivery Details) ──────────────────────────────

class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_line = db.Column(db.String(500), default="")
    city = db.Column(db.String(100), default="")
    state = db.Column(db.String(100), default="")
    pincode = db.Column(db.String(20), default="")
    country = db.Column(db.String(100), default="")
    mobile = db.Column(db.String(20), default="")
    status = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "_id": self.id,
            "address_line": self.address_line,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "country": self.country,
            "mobile": self.mobile,
            "status": self.status,
            "userId": self.user_id,
            "createdAt": self.created_at.isoformat() if self.created_at else "",
            "updatedAt": self.updated_at.isoformat() if self.updated_at else "",
        }

# ── Order ────────────────────────────────────────────────────────

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_details = db.Column(db.JSON)
    payment_status = db.Column(db.String(50), default="CASH ON DELIVERY")
    delivery_address = db.Column(db.JSON, default=dict)
    sub_total_amt = db.Column(db.Float, default=0)
    total_amt = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    product = db.relationship("Product", backref="order_items", lazy=True)

    def to_dict(self):
        return {
            "_id": self.id,
            "orderId": self.order_id,
            "userId": self.user_id,
            "productId": self.product_id,
            "product_details": self.product_details or {},
            "payment_status": self.payment_status or "",
            "delivery_address": self.delivery_address or {},
            "subTotalAmt": self.sub_total_amt,
            "totalAmt": self.total_amt,
            "createdAt": self.created_at.isoformat() if self.created_at else "",
            "updatedAt": self.updated_at.isoformat() if self.updated_at else "",
        }
