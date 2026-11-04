#CREATE USER PROFILE - #3
# Boundary: CreateUserProfilePg
# Methods:
#   create_user_profile(data): checks the input, calls CreateUserProfileC, then shows success or fail
#   display_success(user_profile)
#   display_fail(message)
# Calls: CreateUserProfileC.create_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import CreateUserProfileC

class CreateUserProfilePg:
    def create_user_profile(self, data):
        
        profile_name = data.get("name") if isinstance(data, dict) else None
        
        
        if not isinstance(profile_name, str):
            return self.display_fail("Invalid input format")
            
        profile_name = profile_name.strip()
        description = data.get("description")
        description = description.strip() if isinstance(description, str) else ""

        if not profile_name or not description:
            return self.display_fail("Profile name or description cannot be empty")

        account_type = profile_name.replace(" ", "")

        result = CreateUserProfileC().create_user_profile(profile_name, account_type, description)

        if result is None:
            return self.display_fail("Profile name already exists")
        if not result:  # entity returns False when saving fails
            return self.display_fail()

        return self.display_success(result)

    def display_success(self, user_profile):
        return jsonify({
            "success": True,
            "profile": {
                "profile_id": user_profile.profile_id,
                "name": user_profile.name,
                "account_type": user_profile.account_type,
                "description":user_profile.description,
                "is_suspended": user_profile.is_suspended
            }
        }), 201

    def display_fail(self, message="Create User Profile Failed"):
        return jsonify({
            "success": False,
            "message": message
        }), 400