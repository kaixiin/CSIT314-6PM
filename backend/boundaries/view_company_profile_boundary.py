#VIEW COMPANY PROFILE - #16
# Boundary: ViewCompanyProfilePg
# Methods:
#   view_company_profile(): calls the controller, shows the result
#   display_company(company)
#   display_fail(message, status)

from flask import jsonify, session
from controllers.id_controller import ViewCompanyProfileC


class ViewCompanyProfilePg:
    def view_company_profile(self):
        company = ViewCompanyProfileC().view_company_profile(session["account_id"])
        if company is None:
            return self.display_fail("No company profile yet", 404)
        return self.display_company(company)

    def display_company(self, company):
        return jsonify({"success": True, "company": company.to_dict()}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status