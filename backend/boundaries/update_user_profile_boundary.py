#UPDATE USER PROFILE - #5(#127)
# Boundary: UpdateUserProfilePg
# Methods:
#   update_user_profile(): calls UpdateUserProfileC, then updates the details in the DB 
# Calls: UpdateUserProfileC.update_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import UpdateUserProfileC

class UpdateUserProfilePg:
    def update_user_profile(self, profile_id, data):

        name = data.get('name', None)

        if name is not None:
            account_type = name.replace(" ", "")
        else:
            account_type = None

        description = data.get('description', None)

        if all(v is None for v in [name, account_type, description]):
            return jsonify({
                'success': False,
                'message': 'No fields provided for update'
            }), 200
        
        is_updated = UpdateUserProfileC().update_user_profile(
            profile_id=profile_id,
            name=name,
            account_type=account_type,
            description=description
        )
        
        if is_updated is None:
            return jsonify({
                'success': False,
                'message': f'User profile ID {profile_id} not found'
            }), 200

        if is_updated is False:
            return jsonify({
                'success': False,
                'message': 'Failed to update profile. Duplicate account type or database error'
            }), 200

        return jsonify({
            'success': True,
            'message': f'Profile updated successfully',
        }), 200
