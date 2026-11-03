#VIEW USER PROFILE - #4(#126)
# Boundary: ViewUserProfilePg
# Methods:
#   view_user_profile(): calls ViewUserProfileC, then returns specified profile from DB  
# Calls: ViewUserProfileC.view_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import ViewUserProfileC

class ViewUserProfilePg:
    def view_user_profile(self, profile_id):
        
        profile = ViewUserProfileC().view_user_profile(profile_id)
        
        if profile is None:
            return jsonify({
                'success': False,
                'message': f'User profile ID {profile_id} not found'
            }), 200

        profile_data = [
            {
                'profile_id': profile.profile_id,
                'name': profile.name,
                'account_type': profile.account_type,
                'description': profile.description,
                'is_suspended': profile.is_suspended
            }
        ]

        return jsonify({
            'success': True,
            'message': f'Found profile id {profile_id}',
            'data': profile_data
        }), 200
