# Routes for the Interior Designer company profile stories (role check is in id_routes.py)
#   POST   /api/id/company          - create my company (201)
#   GET    /api/id/company          - view my company (404 if none)
#   PUT    /api/id/company          - update my company
#   DELETE /api/id/company          - delete my company
#   GET    /api/id/companies?q=abc  - browse / search all companies (no q lists all)

from flask import request
from routes.id_routes import id_bp
from boundaries.create_company_profile_boundary import CreateCompanyProfilePg
from boundaries.view_company_profile_boundary import ViewCompanyProfilePg
from boundaries.update_company_profile_boundary import UpdateCompanyProfilePg
from boundaries.delete_company_profile_boundary import DeleteCompanyProfilePg
from boundaries.search_company_profile_boundary import SearchCompanyProfilePg


@id_bp.route("/company", methods=["POST"])
def create_company_profile():
    return CreateCompanyProfilePg().create_company_profile(request.get_json(silent=True))


@id_bp.route("/company", methods=["GET"])
def view_company_profile():
    return ViewCompanyProfilePg().view_company_profile()


@id_bp.route("/company", methods=["PUT"])
def update_company_profile():
    return UpdateCompanyProfilePg().update_company_profile(request.get_json(silent=True))


@id_bp.route("/company", methods=["DELETE"])
def delete_company_profile():
    return DeleteCompanyProfilePg().delete_company_profile()


@id_bp.route("/companies", methods=["GET"])
def search_company_profile():
    return SearchCompanyProfilePg().search_company_profile(request.args.get("q", ""))