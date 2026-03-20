from flask import Blueprint, request, jsonify
from models import db, Address
from auth_middleware import auth_required

address_bp = Blueprint("address", __name__, url_prefix="/api/address")

@address_bp.route("/create", methods=["POST"])
@auth_required
def create_address():
    try:
        data = request.get_json()
        new_address = Address(
            address_line=data.get("address_line", ""),
            city=data.get("city", ""),
            state=data.get("state", ""),
            pincode=data.get("pincode", ""),
            country=data.get("country", ""),
            mobile=data.get("mobile", ""),
            status=True,
            user_id=request.user_id
        )
        db.session.add(new_address)
        db.session.commit()
        return jsonify({
            "message": "Address created successfully",
            "success": True,
            "error": False,
            "data": new_address.to_dict()
        })
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500

@address_bp.route("/get", methods=["GET"])
@auth_required
def get_address():
    try:
        addresses = Address.query.filter_by(user_id=request.user_id, status=True).order_by(Address.created_at.desc()).all()
        return jsonify({
            "message": "List of user addresses",
            "success": True,
            "error": False,
            "data": [a.to_dict() for a in addresses]
        })
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500

@address_bp.route("/update", methods=["PUT"])
@auth_required
def update_address():
    try:
        data = request.get_json()
        address_id = data.get("_id")
        if not address_id:
            return jsonify({"message": "Address _id is required", "error": True, "success": False}), 400

        address = Address.query.filter_by(id=address_id, user_id=request.user_id).first()
        if not address:
            return jsonify({"message": "Address not found", "error": True, "success": False}), 404

        if "address_line" in data: address.address_line = data["address_line"]
        if "city" in data: address.city = data["city"]
        if "state" in data: address.state = data["state"]
        if "pincode" in data: address.pincode = data["pincode"]
        if "country" in data: address.country = data["country"]
        if "mobile" in data: address.mobile = data["mobile"]

        db.session.commit()
        return jsonify({
            "message": "Address updated successfully",
            "success": True,
            "error": False,
            "data": address.to_dict()
        })
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500

@address_bp.route("/disable", methods=["DELETE", "POST", "PUT"])
@auth_required
def disable_address():
    try:
        data = request.get_json()
        address_id = data.get("_id")
        if not address_id:
            return jsonify({"message": "Address _id is required", "error": True, "success": False}), 400

        address = Address.query.filter_by(id=address_id, user_id=request.user_id).first()
        if not address:
            return jsonify({"message": "Address not found", "error": True, "success": False}), 404

        address.status = False
        db.session.commit()
        
        return jsonify({
            "message": "Address disabled successfully",
            "success": True,
            "error": False,
            "data": address.to_dict()
        })
    except Exception as e:
        return jsonify({"message": str(e), "error": True, "success": False}), 500
