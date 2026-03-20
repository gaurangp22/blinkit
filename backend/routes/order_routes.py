import uuid
from flask import Blueprint, request, jsonify
from models import db, Order, CartProduct, Product, Address
from auth_middleware import auth_required

order_bp = Blueprint("order", __name__, url_prefix="/api/order")


@order_bp.route("/cash-on-delivery", methods=["POST"])
@auth_required
def place_order():
    try:
        data = request.get_json()
        list_items = data.get("list_items", [])
        address_data = data.get("delivery_address", {})
        sub_total_amt = data.get("subTotalAmt", 0)
        total_amt = data.get("totalAmt", 0)
        user_id = request.user_id

        if not list_items:
            return jsonify({"message": "Cart is empty", "error": True, "success": False}), 400

        # Address validation
        if not address_data:
            return jsonify({"message": "Delivery address is required", "error": True, "success": False}), 400

        required_addr = {"name": "Full name", "mobile": "Phone number", "address_line": "Address", "city": "City", "state": "State", "pincode": "Pincode"}
        for field, label in required_addr.items():
            val = (address_data.get(field) or "").strip()
            if not val:
                return jsonify({"message": f"{label} is required in delivery address", "error": True, "success": False}), 400

        import re
        pincode = address_data.get("pincode", "").strip()
        if not re.match(r'^\d{6}$', pincode):
            return jsonify({"message": "Pincode must be 6 digits", "error": True, "success": False}), 400

        mobile = re.sub(r'[\s\-\+]', '', address_data.get("mobile", ""))
        if mobile.startswith('91') and len(mobile) == 12:
            mobile = mobile[2:]

        invoice_num = f"INV-{uuid.uuid4().hex[:10].upper()}"
        order_records = []
        for item in list_items:
            product_data = item.get("productId", {})
            product_id = product_data.get("_id")
            product = Product.query.get(int(product_id))
            if not product:
                continue

            qty = item.get("quantity", 1)
            order = Order(
                order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                user_id=user_id,
                product_id=product.id,
                product_details={"name": product.name, "image": product.image, "unit": product.unit, "price": product.price, "discount": product.discount},
                payment_status="CASH ON DELIVERY",
                order_status="Confirmed",
                quantity=qty,
                invoice_number=invoice_num,
                delivery_address=address_data,
                sub_total_amt=sub_total_amt,
                total_amt=total_amt,
            )
            db.session.add(order)
            order_records.append(order)

            # Update stock
            product.stock = max(0, product.stock - qty)

        # Auto-save delivery address if not already saved
        existing_addr = Address.query.filter_by(
            user_id=user_id,
            address_line=address_data.get("address_line", ""),
            city=address_data.get("city", ""),
            pincode=address_data.get("pincode", "")
        ).first()
        if not existing_addr:
            new_addr = Address(
                user_id=user_id,
                address_line=address_data.get("address_line", ""),
                city=address_data.get("city", ""),
                state=address_data.get("state", ""),
                pincode=address_data.get("pincode", ""),
                country=address_data.get("country", "India"),
                mobile=address_data.get("mobile", ""),
                status=True,
            )
            db.session.add(new_addr)

        # Clear cart
        CartProduct.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return jsonify({
            "message": "Order placed successfully",
            "error": False,
            "success": True,
            "data": [o.to_dict() for o in order_records],
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@order_bp.route("/order-list", methods=["GET"])
@auth_required
def order_list():
    try:
        orders = Order.query.filter_by(user_id=request.user_id).order_by(Order.created_at.desc()).all()
        return jsonify({
            "message": "Order list",
            "error": False,
            "success": True,
            "data": [o.to_dict() for o in orders],
        })
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@order_bp.route("/cancel", methods=["PUT"])
@auth_required
def cancel_order():
    """Cancel an order if it's still in Confirmed or Processing status."""
    try:
        data = request.get_json()
        order_id = data.get("orderId")
        
        if not order_id:
            return jsonify({"message": "Order ID is required", "error": True, "success": False}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=request.user_id).first()
        if not order:
            return jsonify({"message": "Order not found", "error": True, "success": False}), 404
        
        cancellable = ["Confirmed", "Processing"]
        if order.order_status not in cancellable:
            return jsonify({"message": f"Cannot cancel order in '{order.order_status}' status", "error": True, "success": False}), 400
        
        order.order_status = "Cancelled"
        
        # Restore stock
        product = Product.query.get(order.product_id)
        if product:
            product.stock += order.quantity
        
        db.session.commit()
        return jsonify({"message": "Order cancelled successfully", "error": False, "success": True, "data": order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@order_bp.route("/reorder", methods=["POST"])
@auth_required
def reorder():
    """Add items from a previous order back to the cart."""
    try:
        data = request.get_json()
        order_id = data.get("orderId")
        
        if not order_id:
            return jsonify({"message": "Order ID is required", "error": True, "success": False}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=request.user_id).first()
        if not order:
            return jsonify({"message": "Order not found", "error": True, "success": False}), 404
        
        product = Product.query.get(order.product_id)
        if not product or product.stock <= 0:
            return jsonify({"message": "Product is currently out of stock", "error": True, "success": False}), 400
        
        # Check if already in cart
        existing = CartProduct.query.filter_by(user_id=request.user_id, product_id=order.product_id).first()
        if existing:
            existing.quantity += 1
        else:
            cart_item = CartProduct(user_id=request.user_id, product_id=order.product_id, quantity=1)
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({"message": "Item added to cart", "error": False, "success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "error": True, "success": False}), 500


@order_bp.route("/track", methods=["POST"])
@auth_required
def track_order():
    """Get tracking details for an order with timeline."""
    try:
        data = request.get_json()
        order_id = data.get("orderId")
        
        if not order_id:
            return jsonify({"message": "Order ID is required", "error": True, "success": False}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=request.user_id).first()
        if not order:
            return jsonify({"message": "Order not found", "error": True, "success": False}), 404
        
        # Generate timeline based on status
        from datetime import timedelta
        statuses_flow = ["Confirmed", "Processing", "Packed", "Shipped", "Out for Delivery", "Delivered"]
        
        current_idx = -1
        if order.order_status == "Cancelled":
            timeline = [
                {"status": "Confirmed", "time": order.created_at.isoformat(), "completed": True},
                {"status": "Cancelled", "time": order.updated_at.isoformat(), "completed": True, "cancelled": True}
            ]
        else:
            if order.order_status in statuses_flow:
                current_idx = statuses_flow.index(order.order_status)
            
            timeline = []
            for i, status in enumerate(statuses_flow):
                entry = {"status": status, "completed": i <= current_idx}
                if i <= current_idx:
                    entry["time"] = (order.created_at + timedelta(hours=i * 2)).isoformat()
                timeline.append(entry)
        
        tracking_data = {
            "order": order.to_dict(),
            "timeline": timeline,
            "estimatedDelivery": (order.created_at + timedelta(hours=12)).isoformat(),
        }
        
        return jsonify({"message": "Tracking details", "error": False, "success": True, "data": tracking_data})
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500


# Stub for Stripe checkout (frontend may call this)
@order_bp.route("/checkout", methods=["POST"])
@auth_required
def checkout():
    return jsonify({"message": "Online payment not available. Use Cash on Delivery.", "error": True, "success": False}), 400
