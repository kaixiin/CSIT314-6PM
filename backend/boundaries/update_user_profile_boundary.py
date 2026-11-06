#UPDATE USER PROFILE - #5(#127)
# Boundary: UpdateUserProfilePg
# Methods:
#   update_user_profile(): checks input with validate_update then calls UpdateUserProfileC, then updates the details in the DB 
# Calls: UpdateUserProfileC.update_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import UpdateUserProfileC
from boundaries.profile_input import validate_update

class UpdateUserProfilePg:
    def update_user_profile(self, profile_id, data):

        fields, error = validate_update(data)
        
        if error:
            return self.display_fail(error)
        
        is_updated = UpdateUserProfileC().update_user_profile(
            profile_id=profile_id,
            **fields  # Unpack validated fields
        )
        
        if is_updated is None:
            return self.display_fail(f'User profile ID {profile_id} not found')
                
        if is_updated is False:
            return self.display_fail('Failed to update profile. Duplicate account type or database error')
            
        return self.display_success()

    def display_success(self):
            return jsonify({
            'success': True,
            'message': f'Profile updated successfully',
        }), 200
                
    def display_fail(self, message="Update User Profile Failed"):
        return jsonify({
            'success': False,
            'message': message
        }), 200