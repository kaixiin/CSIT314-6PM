# Routes for login and logout
#   POST /api/login  - calls UserLoginPg.login()
#   POST /api/logout - calls UserLogoutPg.logout()
#   GET  /api/me     - calls UserLoginPg.current_user(), used when the page loads

from flask import Blueprint, request
from boundaries.user_login_boundary import UserLoginPg
from boundaries.user_logout_boundary import UserLogoutPg

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


@auth_bp.route("/login", methods=["POST"])
def login():
    return UserLoginPg().login(request.get_json(silent=True))


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return UserLogoutPg().logout()


@auth_bp.route("/me", methods=["GET"])
def me():
    return UserLoginPg().current_user()
