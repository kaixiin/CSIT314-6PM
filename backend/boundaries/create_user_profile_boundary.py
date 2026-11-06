#CREATE USER PROFILE - #3
# Boundary: CreateUserProfilePg
# Methods:
#   create_user_profile(data): checks the input with validate_create(), calls CreateUserProfileC, then shows success or fail
#   display_success(user_profile)
#   display_fail(message)
# Calls: CreateUserProfileC.create_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import CreateUserProfileC
from boundaries.profile_input import validate_create

class CreateUserProfilePg:
    def create_user_profile(self, data):
        
        fields, error = validate_create(data)
        
        if error:
            return self.display_fail(error)
        
        result = CreateUserProfileC().create_user_profile(
            name=fields['name'],
            account_type=fields['account_type'],
            description=fields['description']
        )

        if result is None:
            return self.display_fail("Profile name already exists")
        
        if not result: 
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