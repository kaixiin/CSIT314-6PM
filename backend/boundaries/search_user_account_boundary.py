# Boundary: SearchUserAccountPg
# Methods:
#   search_user_account(keyword): checks admin, calls the controller, shows the result
#   display_results(accounts)
#   display_no_results()

from flask import jsonify
from boundaries.user_admin import require_admin
from controllers.search_user_account_controller import SearchUserAccountC


class SearchUserAccountPg:
    def search_user_account(self, keyword):
        denied = require_admin()
        if denied:
            return denied

        keyword = (keyword or "").strip()
        accounts = SearchUserAccountC().search_user_account(keyword)
        if not accounts:
            return self.display_no_results()
        return self.display_results(accounts)

    def display_results(self, accounts):
        return jsonify({"success": True, "count": len(accounts),
                        "accounts": [a.to_dict() for a in accounts]}), 200

    def display_no_results(self):
        return jsonify({"success": True, "count": 0, "accounts": [],
                        "message": "No accounts found"}), 200