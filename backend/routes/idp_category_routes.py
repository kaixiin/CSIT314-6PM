# Routes for the IDP category stories
#   PM only:
#     POST  /api/pm/categories                      - create 
#     PUT   /api/pm/categories/<category_id>        - update
#     PATCH /api/pm/categories/<category_id>/status - suspend,
#     GET   /api/categories?q=keyword               - search 
#     GET   /api/categories/<category_id>           - view

from flask import request
from routes.pm_routes import pm_bp
from boundaries.create_idp_category_boundary import CreateIDPCategoryPg
from boundaries.update_idp_category_boundary import UpdateIDPCategoryPg
from boundaries.suspend_idp_category_boundary import SuspendIDPCategoryPg
from boundaries.view_idp_category_boundary import ViewIDPCategoryPg
from boundaries.search_idp_category_boundary import SearchIDPCategoryPg


@pm_bp.route("/categories", methods=["POST"])
def create_idp_category():
    return CreateIDPCategoryPg().create_idp_category(request.get_json(silent=True))


@pm_bp.route("/categories/<int:category_id>", methods=["PUT"])
def update_idp_category(category_id):
    return UpdateIDPCategoryPg().update_idp_category(category_id, request.get_json(silent=True))


@pm_bp.route("/categories/<int:category_id>/status", methods=["PATCH"])
def suspend_idp_category(category_id):
    return SuspendIDPCategoryPg().suspend_idp_category(category_id, request.get_json(silent=True))

@pm_bp.route("/categories", methods=["GET"])
def search_idp_category():
    return SearchIDPCategoryPg().search_idp_category(request.args.get("q", ""))


@pm_bp.route("/categories/<int:category_id>", methods=["GET"])
def view_idp_category(category_id):
    return ViewIDPCategoryPg().view_idp_category(category_id)
