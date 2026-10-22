# Boundary: UserLogoutPg
# Methods:
#   logout(): ends the session, then shows success
#   display_success()
# Calls: UserLogoutC.logout() in controllers/user_logout_controller.py

from flask import session, jsonify
from controllers.user_logout_controller import UserLogoutC


class UserLogoutPg:
    def logout(self):
        UserLogoutC().logout()
        session.clear()
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True}), 200