from flask import Blueprint, request, session, jsonify
from boundaries.create_user_profile_boundary import CreateUserProfilePg

# All routes here will automatically require "UserAdmin"
admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.before_request
def restrict_to_admins():
    if request.method == "OPTIONS":
        return
    
    if not session.get("account_id"):
        return jsonify({"success": False, "message": "Login required"}), 401
        
    if session.get("account_type") != "UserAdmin":
        return jsonify({"success": False, "message": "Access denied: Admins only"}), 403

# Admin-only functions
@admin_bp.route("/profiles", methods=["POST", "OPTIONS"])
def admin_create_profile():
    if request.method == "OPTIONS":
        return "", 200
    form_data = request.get_json(silent=True) or {}
    return CreateUserProfilePg().create_user_profile(form_data)
