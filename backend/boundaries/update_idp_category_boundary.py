# UPDATE IDP CATEGORY - #43
# Boundary: UpdateIDPCategoryPg
# Methods: update_idp_category(category_id, data), display_success(), display_fail(message, status)

from flask import jsonify, session
from controllers.pm_controller import (
    CreateIDPCategoryC, ViewIDPCategoryC, UpdateIDPCategoryC,
    SuspendIDPCategoryC, SearchIDPCategoryC)
from boundaries.idp_category_input import read_category_fields
class UpdateIDPCategoryPg:
    def update_idp_category(self, category_id, data):
        fields, error = read_category_fields(data)
        if error:
            return self.display_fail(error)
        updated = UpdateIDPCategoryC().update_idp_category(
            category_id, fields["name"], fields["description"])
        if updated is None:
            return self.display_fail("Category not found", 404)
        if not updated:
            return self.display_fail("Update failed. The category name may already be used.")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Category updated successfully"}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status