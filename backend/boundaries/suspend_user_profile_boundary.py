#SUSPEND USER PROFILE - #6 (#128)
# Boundary: SuspendUserProfilePg
# Methods:
#   suspend_user_profile(profile_id): checks the input, calls SuspendUserProfileC, then shows success or fail
#   display_success(user_profile)
#   display_fail(message, status)
# Calls: SuspendUserProfileC.create_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import SuspendUserProfileC

class SuspendUserProfilePg:
    def suspend_user_profile(self, profile_id, data):
        
        is_suspended = data.get('is_suspended')
        
        status = SuspendUserProfileC().suspend_user_profile(
            profile_id,
            is_suspended=is_suspended
        )
        
        if status is None:
            return self.display_fail(f'User profile ID {profile_id} not found', 404)

        if status is False:
            if is_suspended == True:
                        message = 'suspend'
            elif is_suspended == False:
                        message = 'reactivate'
            return self.display_fail(f'Failed to {message} profile ID {profile_id}.')
                
        if is_suspended == True:
                message = 'suspended'
        elif is_suspended == False:
                message = 'reactivated'

        return self.display_success(profile_id, message)

    def display_success(self, profile_id, message):
                return jsonify({
                    'success': True,
                    'message': f'Profile ID {profile_id} successfully {message}'
                }), 200
        
    def display_fail(self, message="Suspend User Profile Failed", status=400):
        return jsonify({
                        'success': False,
                        'message': message
        }), status