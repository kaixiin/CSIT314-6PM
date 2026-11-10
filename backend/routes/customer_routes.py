from flask import Blueprint, request, session, jsonify
from boundaries.cust_search_idp_boundary import CustSearchIDPPg


# All routes here will automatically require "UserAdmin"
cust_bp = Blueprint("customer", __name__, url_prefix="/api/customer")

@cust_bp.before_request
def restrict_to_admins():
    if request.method == "OPTIONS":
        return
    
    if not session.get("account_id"):
        return jsonify({"success": False, "message": "Login required"}), 401
        
    if session.get("account_type") != "Customer":
        return jsonify({"success": False, "message": "Access denied: Customer only"}), 403

#Customer access functions
@cust_bp.route("/idps", methods=["GET"])
def search_idp():
    """Public search for all IDPs (for customers)"""
    return CustSearchIDPPg().search_idp()