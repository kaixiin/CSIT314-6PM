# Base blueprint for the Interior Designer role.
# Every URL under /api/id needs a logged-in InteriorDesigner (401 / 403 otherwise).

from flask import Blueprint, request
from boundaries.interior_designer import require_interior_designer

id_bp = Blueprint("interior_designer", __name__, url_prefix="/api/id")

@id_bp.before_request
def check_interior_designer():
    if request.method == "OPTIONS":      # browser preflight carries no cookie
        return None
    return require_interior_designer()