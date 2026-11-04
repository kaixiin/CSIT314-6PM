from flask import session, jsonify

def require_admin():
    """Return an error response if the user is not a logged-in UserAdmin, otherwise None."""
    if session.get("account_id") is None:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    if session.get("account_type") != "UserAdmin":
        return jsonify({"success": False, "message": "Not allowed"}), 403
    return None