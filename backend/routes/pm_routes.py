# Base blueprint for the Platform Manager role.
# Every URL under /api/pm needs a logged-in PlatformManager

from flask import Blueprint, request
from boundaries.platform_manager import require_platform_manager

pm_bp = Blueprint("platform_manager", __name__, url_prefix="/api/pm")

@pm_bp.before_request
def check_platform_manager():
    if request.method == "OPTIONS":      # browser preflight carries no cookie
        return None
    return require_platform_manager()