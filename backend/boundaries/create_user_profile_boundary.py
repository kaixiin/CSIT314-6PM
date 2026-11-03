# Boundary: CreateUserProfilePg
# Methods:
#   login(data): checks the input, calls UserLoginC, then shows success or fail
#   display_success(account)
#   display_fail()
# Calls: CreateUserProfileC.execute() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import CreateUserProfileC

class CreateUserProfilePg:
    def create_user_profile(self, data):
        
        profile_name = data.get("name") if isinstance(data, dict) else None
        
        
        if not isinstance(profile_name, str):
            return self.display_fail("Invalid input format")
            
        profile_name = profile_name.strip()
        description = data.get("description") if isinstance(data, dict) else None
        description = description.strip()

        if not profile_name or not description:
            return self.display_fail("Profile name or description cannot be empty")

        account_type = profile_name.replace(" ", "")

        result = CreateUserProfileC().create_user_profile(profile_name, account_type, description)

        if result is None:
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

    def display_fail(self):
        return jsonify({
            "success": False, 
            "message": "Create User Profile Failed"
        }), 400