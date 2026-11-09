# CREATE IDP CATEGORY - #41
# Boundary: CreateIDPCategoryPg
# Methods: create_idp_category(data), display_success(), display_fail(message, status)

from flask import jsonify, session
from controllers.pm_controller import (
    CreateIDPCategoryC, ViewIDPCategoryC, UpdateIDPCategoryC,
    SuspendIDPCategoryC, SearchIDPCategoryC)
from boundaries.idp_category_input import read_category_fields

class CreateIDPCategoryPg:
    def create_idp_category(self, data):
        fields, error = read_category_fields(data)
        if error:
            return self.display_fail(error)
        created = CreateIDPCategoryC().create_idp_category(fields["name"], fields["description"])
        if not created:
            return self.display_fail("Create failed. The category name may already exist.")
        return self.display_success()

    def display_success(self):
        return jsonify({"success": True, "message": "Category created"}), 201

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status