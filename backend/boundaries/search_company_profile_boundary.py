# SEARCH COMPANY PROFILE - #19
# Boundary: SearchCompanyProfilePg
# Methods:
#   search_company_profile(keyword): calls the controller, shows the result
#   display_results(companies)
#   display_no_results()

from flask import jsonify, session
from controllers.search_company_profile_controller import SearchCompanyProfileC


class SearchCompanyProfilePg:
    def search_company_profile(self, keyword):
        keyword = (keyword or "").strip()
        companies = SearchCompanyProfileC().search_company_profile(keyword, session["account_id"])
        if not companies:
            return self.display_no_results()
        return self.display_results(companies)

    def display_results(self, companies):
        return jsonify({"success": True, "count": len(companies),
                        "companies": [c.to_dict() for c in companies]}), 200

    def display_no_results(self):
        return jsonify({"success": True, "count": 0, "companies": [],
                        "message": "No companies found"}), 200