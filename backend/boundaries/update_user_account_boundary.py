# Boundary: UpdateUserAccountPg
# Methods:
#   update_user_account(account_id, data): checks admin and input, calls the controller
#   display_success()
#   display_fail(message)

from flask import jsonify
from boundaries.user_admin import require_admin
from boundaries.account_input import read_account_fields
from controllers.admin_controller import UpdateUserAccountC


class UpdateUserAccountPg:
    def update_user_account(self, account_id, data):
        denied = require_admin()
        if denied:
            return denied

        fields, error = read_account_fields(data, need_password=False)
        if error:
            return self.display_fail(error)

        updated = UpdateUserAccountC().update_user_account(
            account_id, fields["username"], fields["email"], fields["profile_id"])
        if not updated:
            return self.display_fail(
                "Update failed. The account or profile may not exist, or the username or email is already used.")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Account updated"}), 200

    def display_fail(self, message):
        return jsonify({"success": False, "message": message}), 400