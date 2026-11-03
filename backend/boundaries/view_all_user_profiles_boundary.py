#VIEW ALL USER PROFILE 
# Boundary: ViewAllUserProfilePg
# Methods:
#   view_all_user_profiles(): calls ViewAllUserProfileC, then returns data from DB
#   
# Calls: ViewAllUserProfileC.view_all_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import ViewAllUserProfileC

class ViewAllUserProfilePg:
    def view_all_user_profiles(self):
        
        all_profiles = ViewAllUserProfileC.view_all_user_profiles()
        
        
        if all_profiles is None:
            return jsonify({
                'success': False,
                'message': 'Error retrieving user profiles'
            }), 200

        if len(all_profiles) == 0:
            return jsonify({
                'success': True,
                'message': 'No user profiles found',
                'data': []
            }), 200

        all_profiles_data = [
            {
                'profile_id': p.profile_id,
                'name': p.name,
                'account_type': p.account_type,
                'description': p.description,
                'is_suspended': p.is_suspended
            }
            for p in all_profiles
        ]

        return jsonify({
            'success': True,
            'message': f'Found {len(all_profiles)} profile(s)',
            'data': all_profiles_data
        }), 200

    