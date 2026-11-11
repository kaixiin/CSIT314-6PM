# VIEW IDP CATEGORY - #42
# Boundary: ViewIDPCategoryPg
# Methods: view_idp_category(category_id), display_category(category, idps), display_fail(message, status)

from flask import jsonify, session
from controllers.pm_controller import (
    CreateIDPCategoryC, ViewIDPCategoryC, UpdateIDPCategoryC,
    SuspendIDPCategoryC, SearchIDPCategoryC)

class ViewIDPCategoryPg:
    def view_idp_category(self, category_id):
        category = ViewIDPCategoryC().view_idp_category(category_id)
        if category is None:
            return self.display_fail("Category not found", 404)
        return self.display_category(category, ViewIDPCategoryC().idps_in_category(category_id))

    def display_category(self, category, idps):
        return jsonify({"success": True, "category": {**category.to_dict(), "idps": idps}}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status