# Routes for login and logout
#   POST /api/login  - calls UserLoginC.verify_login()
#   POST /api/logout - calls UserLogoutC.logout()

from flask import Blueprint, request, jsonify
from controllers.user_login_controller import UserLoginC

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    account = UserLoginC().verify_login(data.get("username"), data.get("password"))

    if account is None:
        return jsonify({"success": False, "message": "Login failed"}), 401

    return jsonify({
        "success": True,
        "account": {
            "account_id": account.account_id,
            "username": account.username,
            "profile_id": account.profile_id,
        },
    }), 200