from flask import Blueprint, request, session, jsonify
from boundaries.cust_search_idp_boundary import CustSearchIDPPg
from boundaries.cust_view_idp_boundary import CustViewIDPPg
from boundaries.shortlist_idp_boundary import ShortlistIDPPg
from boundaries.view_shortlisted_idp_boundary import ViewShortlistedIDPPg
from boundaries.search_shortlisted_idp_boundary import SearchShortlistedIDPPg
from boundaries.id_view_idp_category_boundary import ViewCategoriesPg


# All routes here will automatically require "UserAdmin"
cust_bp = Blueprint("customer", __name__, url_prefix="/api/customer")

@cust_bp.before_request
def restrict_to_customer():
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

@cust_bp.route("/idps/<idp_id>", methods=["GET"])
def view_idp(idp_id):
    return CustViewIDPPg().view_idp(idp_id)

@cust_bp.route("/idps/<idp_id>/favourites", methods=["POST", "OPTIONS"])
def save_favourite(idp_id):
    if request.method == "OPTIONS":
        return "", 200
    
    return ShortlistIDPPg().save_favourite(idp_id)

@cust_bp.route("/favourites", methods=["GET"])
def view_or_search_shortlisted():
  
    keyword = request.args.get("q", "").strip()
    
    if keyword:
        # search mode - call search boundary
        return SearchShortlistedIDPPg().search_favourites(keyword)
    else:
        # view all mode - call view boundary
        return ViewShortlistedIDPPg().view_favourite_list()

@cust_bp.route("/categories", methods=["GET"])
def view_categories():
    return ViewCategoriesPg().view_categories()
