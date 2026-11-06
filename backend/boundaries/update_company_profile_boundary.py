# UPDATE COMPANY PROFILE - #17
# Boundary: UpdateCompanyProfilePg
# Methods:
#   update_company_profile(data): checks input, calls the controller, shows the result
#   display_success()
#   display_fail(message, status)

from flask import jsonify, session
from boundaries.company import read_company_form, remove_logo
from controllers.update_company_profile_controller import UpdateCompanyProfileC


class UpdateCompanyProfilePg:
    def update_company_profile(self, data):
        fields, error = read_company_form(data)    # logo is optional: leave it out to keep the old one
        if error:
            return self.display_fail(error)

        updated = UpdateCompanyProfileC().update_company_profile(
            session["account_id"], fields["company_name"], fields["description"],
            fields["address"], fields["contact_number"], fields["email"], fields["logo"])
        if updated is None:
            remove_logo(fields["logo"])
            return self.display_fail("No company profile yet", 404)
        if not updated:
            remove_logo(fields["logo"])
            return self.display_fail("Update failed. The company name may already be taken.")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Company profile updated successfully"}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status