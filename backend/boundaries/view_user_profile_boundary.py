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
            return self.display_fail(f"Profile ID {profile_id} cannot be found")

        return self.display_user_profile(profile)

    def display_user_profile(self, profile):
        return jsonify({
            "success": True,
            "profile": {
                "profile_id": profile.profile_id,
                "name": profile.name,
                "account_type": profile.account_type,
                "description":profile.description,
                "is_suspended": profile.is_suspended
            }
        }), 200

    def display_fail(self, message="Find User Profile Failed"):
        return jsonify({
                        'success': False,
                        'message': message
        }), 200