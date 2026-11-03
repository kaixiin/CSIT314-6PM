# Boundary: SuspendUserAccountPg
# Methods:
#   suspend_user_account(account_id): checks admin, calls the controller, shows the result
#   display_success()
#   display_fail(message)

from flask import jsonify, session
from boundaries.user_admin import require_admin
from controllers.suspend_user_account_controller import SuspendUserAccountC


class SuspendUserAccountPg:
    def suspend_user_account(self, account_id):
        denied = require_admin()
        if denied:
            return denied

        # an admin must not lock themselves out
        if account_id == session.get("account_id"):
            return self.display_fail("You cannot suspend your own account")

        if not SuspendUserAccountC().suspend_user_account(account_id):
            return self.display_fail("Suspend failed. The account does not exist.")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Account suspended"}), 200

    def display_fail(self, message):
        return jsonify({"success": False, "message": message}), 400