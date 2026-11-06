#SEARCH USER PROFILE - #7
# Boundary: SearchUserProfilePg
# Methods:
#   search_user_profile(keyword): c calls SearchUserProfileC, then shows success or fail
#   display_success(results)
#   display_fail(message)
# Calls: SearchUserProfileC.search_user_profile() in controllers/admin_controller.py

from flask import jsonify
from controllers.admin_controller import SearchUserProfileC

class SearchUserProfilePg:
    def search_user_profiles(self, data):
        print('insearch')
        keyword = data.get("q") if isinstance(data, dict) else None
        
        if not isinstance(keyword, str):
            return jsonify({
                "success": False,
                "message": "Search keyword is required"
            }), 200

        keyword = keyword.strip()

        if not keyword:
            return self.display_fail('Search keyword cannot be empty')

        results = SearchUserProfileC().search_user_profiles(keyword)

        if results is None:
            return self.display_fail('Failed to search user profiles')

        profiles_data = [
            {
                "profile_id": p.profile_id,
                "name": p.name,
                "account_type": p.account_type,
                "description": p.description,
                "is_suspended": p.is_suspended
            }
            for p in results
        ]

        return self.display_success(profiles_data)

    def display_success(self, results):
                return jsonify({
                    "success": True,
                    "message": f"Found {len(results)} profile(s)",
                    "data": results
                }), 200
        
    def display_fail(self, message="Search User Profile Failed"):
        return jsonify({
                        'success': False,
                        'message': message
        }), 200