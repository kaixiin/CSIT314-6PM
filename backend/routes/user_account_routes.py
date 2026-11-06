# Routes for the User Admin user account stories
#   POST  /api/admin/accounts                    - create  (#8)
#   GET   /api/admin/accounts?q=abc              - search  (#12, empty q lists all)
#   GET   /api/admin/accounts/<id>               - view    (#9)
#   PUT   /api/admin/accounts/<id>               - update  (#10)
#   PATCH /api/admin/accounts/<id>/status        - suspend / reactivate (#11)

from flask import Blueprint, request
from boundaries.create_user_account_boundary import CreateUserAccountPg
from boundaries.view_user_account_boundary import ViewUserAccountPg
from boundaries.update_user_account_boundary import UpdateUserAccountPg
from boundaries.suspend_user_account_boundary import SuspendUserAccountPg
from boundaries.search_user_account_boundary import SearchUserAccountPg

user_account_bp = Blueprint("user_account", __name__, url_prefix="/api/admin")


@user_account_bp.route("/accounts", methods=["POST"])
def create_user_account():
    return CreateUserAccountPg().create_user_account(request.get_json(silent=True))


@user_account_bp.route("/accounts", methods=["GET"])
def search_user_account():
    return SearchUserAccountPg().search_user_account(request.args.get("q", ""))


@user_account_bp.route("/accounts/<int:account_id>", methods=["GET"])
def view_user_account(account_id):
    return ViewUserAccountPg().view_user_account(account_id)


@user_account_bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_user_account(account_id):
    return UpdateUserAccountPg().update_user_account(account_id, request.get_json(silent=True))


@user_account_bp.route("/accounts/<int:account_id>/status", methods=["PATCH"])
def suspend_user_account(account_id):
    return SuspendUserAccountPg().suspend_user_account(account_id, request.get_json(silent=True))
