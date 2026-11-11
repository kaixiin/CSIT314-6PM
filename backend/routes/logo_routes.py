# GET /api/logos/ and /api/idp-images/ - serve uploaded company logos and IDP photos

from flask import Blueprint, send_from_directory
from boundaries.company import UPLOAD_FOLDER

logo_bp = Blueprint("logo", __name__, url_prefix="/api")


@logo_bp.route("/logos/<path:filename>", methods=["GET"])
def logo_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@logo_bp.route("/idp-images/<path:filename>", methods=["GET"])
def idp_image_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
