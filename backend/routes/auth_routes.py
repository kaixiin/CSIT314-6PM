# Routes for login and logout
#   POST /api/login  - calls UserLoginC.verify_login()
#   POST /api/logout - calls UserLogoutC.logout()

from flask import Blueprint, request, jsonify, session
from controllers.user_login_controller import UserLoginC
from controllers.user_logout_controller import UserLogoutC

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        data = {}

    account = UserLoginC().verify_login(data.get("username"), data.get("password"))

    if account is None:
        return jsonify({"success": False, "message": "Login failed"}), 401

    session.clear()
    session["account_id"] = account.account_id
    session["profile_id"] = account.profile_id

    profile = account.profile
    return jsonify({
        "success": True,
        "account": {
            "account_id": account.account_id,
            "username": account.username,
            "profile_id": account.profile_id,
            "account_type": profile.account_type,
            "permissions": profile.permissions,
        },
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    UserLogoutC().logout()
    return jsonify({"success": True}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    account_id = session.get("account_id")
    if account_id is None:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    return jsonify({
        "success": True,
        "account_id": account_id,
        "profile_id": session.get("profile_id"),
    }), 200