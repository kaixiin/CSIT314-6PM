# Boundary: SuspendUserAccountPg
# Methods:
#   suspend_user_account(account_id, data): checks admin and input, calls the controller, shows the result
#   display_success(is_suspended)
#   display_fail(message)

from flask import jsonify, session
from boundaries.user_admin import require_admin
from controllers.suspend_user_account_controller import SuspendUserAccountC


class SuspendUserAccountPg:
    def suspend_user_account(self, account_id, data):
        denied = require_admin()
        if denied:
            return denied

        # body: {"is_suspended": true} to suspend, false to reactivate
        is_suspended = (data or {}).get("is_suspended")
        if not isinstance(is_suspended, bool):
            return self.display_fail("is_suspended must be true or false")

        # an admin must not lock themselves out
        if is_suspended and account_id == session.get("account_id"):
            return self.display_fail("You cannot suspend your own account")

        if not SuspendUserAccountC().suspend_user_account(account_id, is_suspended):
            return self.display_fail("Update failed. The account does not exist.")
        return self.display_success(is_suspended)

    def display_success(self, is_suspended):
        message = "Account suspended" if is_suspended else "Account reactivated"
        return jsonify({"success": True, "message": message}), 200

    def display_fail(self, message):
        return jsonify({"success": False, "message": message}), 400
