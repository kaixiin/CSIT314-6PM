# Boundary: ViewUserAccountPg
# Methods:
#   view_user_account(account_id): checks admin, calls the controller, shows the result
#   display_account(account)
#   display_fail(message, status)

from flask import jsonify
from boundaries.user_admin import require_admin
from controllers.view_user_account_controller import ViewUserAccountC


class ViewUserAccountPg:
    def view_user_account(self, account_id):
        denied = require_admin()
        if denied:
            return denied

        account = ViewUserAccountC().view_user_account(account_id)
        if account is None:
            return self.display_fail("Account not found", 404)
        return self.display_account(account)

    def display_account(self, account):
        return jsonify({"success": True, "account": account.to_dict()}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status