# SUSPEND IDP CATEGORY - #44
# Boundary: SuspendIDPCategoryPg
# Methods: suspend_idp_category(category_id, data), display_success(), display_fail(message, status)

from flask import jsonify, session
from controllers.pm_controller import (
    CreateIDPCategoryC, ViewIDPCategoryC, UpdateIDPCategoryC,
    SuspendIDPCategoryC, SearchIDPCategoryC)

class SuspendIDPCategoryPg:
    def suspend_idp_category(self, category_id, data):
        data = data if isinstance(data, dict) else {}
        
        # 1. Replaced the strict "is not True" check with a type check
        is_suspended = data.get("is_suspended")
        if not isinstance(is_suspended, bool):
            return self.display_fail('Please send {"is_suspended": true} or {"is_suspended": false}.')
            
        # 2. Pass the boolean to the controller
        suspended = SuspendIDPCategoryC().suspend_idp_category(category_id, is_suspended)
        
        if suspended is None:
            return self.display_fail("Category not found", 404)
        if not suspended:
            # 3. Made the error message more generic
            return self.display_fail("Status update failed")
            
        return self.display_success(is_suspended)

    # 4. Updated display_success to say "suspended" or "reactivated" based on the input
    def display_success(self, is_suspended):
        status = "suspended" if is_suspended else "reactivated"
        return jsonify({"success": True, "message": f"Category {status}"}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status