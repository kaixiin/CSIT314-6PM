# Boundary: CreateUserAccountPg
# Methods:
#   create_user_account(data): checks admin and input, calls the controller, shows the result
#   display_success()
#   display_fail(message)

from flask import jsonify
from boundaries.user_admin import require_admin
from boundaries.account_input import read_account_fields
from controllers.admin_controller import CreateUserAccountC


class CreateUserAccountPg:
    def create_user_account(self, data):
        denied = require_admin()
        if denied:
            return denied

        fields, error = read_account_fields(data, need_password=True)
        if error:
            return self.display_fail(error)

        created = CreateUserAccountC().create_user_account(
            fields["username"], fields["password"], fields["email"], fields["profile_id"])
        if not created:
            return self.display_fail(
                "Create failed. The username or email may already exist, or the profile does not exist.")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Account created"}), 201

    def display_fail(self, message):
        return jsonify({"success": False, "message": message}), 400