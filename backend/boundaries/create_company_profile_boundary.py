# CREATE COMPANY PROFILE - #15
# Boundary: CreateCompanyProfilePg
# Methods:
#   create_company_profile(data): checks input, calls the controller, shows the result
#   display_success()
#   display_fail(message, status)

from flask import jsonify, session
from boundaries.company import read_company_form, remove_logo
from controllers.create_company_profile_controller import CreateCompanyProfileC


class CreateCompanyProfilePg:
    def create_company_profile(self, data):
        fields, error = read_company_form(data)
        if error:
            return self.display_fail(error)

        created = CreateCompanyProfileC().create_company_profile(
            session["account_id"], fields["company_name"], fields["description"],
            fields["address"], fields["contact_number"], fields["email"], fields["logo"])
        if not created:
            remove_logo(fields["logo"])
            return self.display_fail(
                "Create failed. You may already have a company profile, or the company name is taken.")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Company profile created"}), 201

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status