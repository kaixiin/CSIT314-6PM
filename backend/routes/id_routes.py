# Base blueprint for the Interior Designer role.
# Every URL under /api/id needs a logged-in InteriorDesigner (401 / 403 otherwise).

from flask import Blueprint, request, jsonify, session
from boundaries.interior_designer import require_interior_designer
from boundaries.create_idp_boundary import CreateIDPPg
from boundaries.id_view_idp_boundary import IDViewIDPPg
from boundaries.update_idp_boundary import UpdateIDPPg
from boundaries.delete_idp_boundary import DeleteIDPPg
from boundaries.id_search_idp_boundary import IDSearchIDPPg
from boundaries.view_idp_stats_boundary import ViewIDPStatsPg
from boundaries.id_view_idp_category_boundary import ViewCategoriesPg


id_bp = Blueprint("interior_designer", __name__, url_prefix="/api/id")

@id_bp.before_request
def check_interior_designer():
    if request.method == "OPTIONS":     
        return None
    return require_interior_designer()

@id_bp.route("/idps", methods=["POST"])
def create_idp():
    return CreateIDPPg().create_idp(request.get_json(silent=True))

@id_bp.route("/idps/<idp_id>", methods=["GET"])
def id_view_idp(idp_id):
    return IDViewIDPPg().id_view_idp(idp_id)

@id_bp.route("/idps/<idp_id>", methods=["PUT", "OPTIONS"])
def update_idp(idp_id):

    data = request.get_json(silent=True) or {}
    return UpdateIDPPg().update_idp(idp_id, data)

@id_bp.route("/idps/<idp_id>", methods=["DELETE", "OPTIONS"])
def delete_idp(idp_id):
    if request.method == "OPTIONS":
        return "", 200
    return DeleteIDPPg().delete_idp(idp_id)

@id_bp.route("/idps", methods=["GET"])
def id_search_idp():
    return IDSearchIDPPg().search_my_idp()

@id_bp.route("/idps/<idp_id>/stats", methods=["GET"])
def view_idp_stats(idp_id):
    return ViewIDPStatsPg().view_idp_stats(idp_id)

@id_bp.route("/categories", methods=["GET"])
def view_categories():
    return ViewCategoriesPg().view_categories()