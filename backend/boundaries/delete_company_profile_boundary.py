# DELETE COMPANY PROFILE - #17
# Boundary: DeleteCompanyProfilePg
# Methods:
#   delete_company_profile(): calls the controller, shows the result
#   display_success()
#   display_fail(message, status)
# (the "Are you sure?" dialogue is shown by the page, so only a confirmed request reaches here)

from flask import jsonify, session
from controllers.id_controller import DeleteCompanyProfileC


class DeleteCompanyProfilePg:
    def delete_company_profile(self):
        deleted = DeleteCompanyProfileC().delete_company_profile(session["account_id"])
        if deleted is None:
            return self.display_fail("No company profile yet", 404)
        if not deleted:
            return self.display_fail("Delete failed")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Company profile deleted successfully"}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status