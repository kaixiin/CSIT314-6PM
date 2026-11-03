# Routes for the User Admin user account stories
#   POST /api/user-accounts                    - create
#   GET  /api/user-accounts?search=abc         - search (empty search lists all)
#   GET  /api/user-accounts/<id>               - view
#   PUT  /api/user-accounts/<id>               - update
#   POST /api/user-accounts/<id>/suspend       - suspend

from flask import Blueprint, request
from boundaries.create_user_account_boundary import CreateUserAccountPg
from boundaries.view_user_account_boundary import ViewUserAccountPg
from boundaries.update_user_account_boundary import UpdateUserAccountPg
from boundaries.suspend_user_account_boundary import SuspendUserAccountPg
from boundaries.search_user_account_boundary import SearchUserAccountPg

admin_bp = Blueprint("user_account", __name__, url_prefix="/api")


@admin_bp.route("/user-accounts", methods=["POST"])
def create_user_account():
    return CreateUserAccountPg().create_user_account(request.get_json(silent=True))


@admin_bp.route("/user-accounts", methods=["GET"])
def search_user_account():
    return SearchUserAccountPg().search_user_account(request.args.get("search", ""))


@admin_bp.route("/user-accounts/<int:account_id>", methods=["GET"])
def view_user_account(account_id):
    return ViewUserAccountPg().view_user_account(account_id)


@admin_bp.route("/user-accounts/<int:account_id>", methods=["PUT"])
def update_user_account(account_id):
    return UpdateUserAccountPg().update_user_account(account_id, request.get_json(silent=True))


@admin_bp.route("/user-accounts/<int:account_id>/suspend", methods=["POST"])
def suspend_user_account(account_id):
    return SuspendUserAccountPg().suspend_user_account(account_id)