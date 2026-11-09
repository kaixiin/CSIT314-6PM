# SEARCH IDP CATEGORY - #45
# Boundary: SearchIDPCategoryPg
# Methods: search_idp_category(keyword), display_results(categories), display_no_results()

from flask import jsonify, session
from controllers.pm_controller import (
    CreateIDPCategoryC, ViewIDPCategoryC, UpdateIDPCategoryC,
    SuspendIDPCategoryC, SearchIDPCategoryC)

class SearchIDPCategoryPg:
    def search_idp_category(self, keyword):
        keyword = (keyword or "").strip()
        categories = SearchIDPCategoryC().search_idp_category(keyword)
        if not categories:
            return self.display_no_results()
        return self.display_results(categories)

    def display_results(self, categories):
        return jsonify({"success": True, "count": len(categories),
                        "categories": [c.to_dict() for c in categories]}), 200

    def display_no_results(self):
        return jsonify({"success": True, "count": 0, "categories": [],
                        "message": "No categories found"}), 200