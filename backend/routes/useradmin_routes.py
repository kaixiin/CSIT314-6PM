from flask import Blueprint, request, session, jsonify
from boundaries.create_user_profile_boundary import CreateUserProfilePg
from boundaries.view_all_user_profiles_boundary import ViewAllUserProfilePg
from boundaries.view_user_profile_boundary import ViewUserProfilePg
from boundaries.update_user_profile_boundary import UpdateUserProfilePg
from boundaries.suspend_user_profile_boundary import SuspendUserProfilePg
from boundaries.search_user_profile_boundary import SearchUserProfilePg

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
def admin_create_user_profile():
    if request.method == "OPTIONS":
        return "", 200
    form_data = request.get_json(silent=True) or {}
    return CreateUserProfilePg().create_user_profile(form_data)

@admin_bp.route("/profiles", methods=["GET"])
def admin_view_all_user_profiles():
    return ViewAllUserProfilePg().view_all_user_profiles()

@admin_bp.route("/profiles/<profile_id>", methods=["GET"])
def admin_view_single_user_profile(profile_id):
    """View individual user profile by ID"""
    return ViewUserProfilePg().view_user_profile(profile_id)

@admin_bp.route("/profiles/<profile_id>", methods=["PUT","OPTIONS"])
def admin_update_user_profile(profile_id):
    if request.method == "OPTIONS":
            return "", 200

    data = request.get_json(silent=True) or {}
    return UpdateUserProfilePg().update_user_profile(profile_id, data)

@admin_bp.route("/profiles/<profile_id>/status", methods=["PATCH"])
def admin_suspend_user_profile(profile_id):

    data = request.get_json(silent=True) or {}
    return SuspendUserProfilePg().suspend_user_profile(profile_id, data)

@admin_bp.route("/profiles?q=", methods=["GET"])
def admin_search_user_profile(profile_id):

    data = request.get_json(silent=True) or {}
    return SearchUserProfilePg().search_user_profiles(profile_id, data)
