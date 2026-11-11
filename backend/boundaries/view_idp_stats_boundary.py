# VIEW IDP STATS - #37, 38
# Boundary: ViewIDPStatsPg
# Methods: view_idp_stats(category_id), display_category(category), display_fail(message, status)
from flask import jsonify, session
from controllers.id_controller import IDViewIDPC, ViewIDPViewCountC, ViewIDPShortlistCountC

class ViewIDPStatsPg:
    
    def view_idp_stats(self, idp_id):
    
        account_id = session.get("account_id")
        
        if not account_id:
            return self.display_fail("Login required", 401)
        
        # Returns None when the project does not exist or belongs to another designer
        idp = IDViewIDPC().id_view_idp(idp_id, account_id)
        
        if idp is None:
            return self.display_fail(f"IDP with ID {idp_id} not found", 404)
        
        view_count = ViewIDPViewCountC().count_views(idp_id)
        shortlist_count = ViewIDPShortlistCountC().count_shortlists(idp_id)
        
        return self.display_result(view_count, shortlist_count)
    
    def display_result(self, view_count, shortlist_count):
        return jsonify({
            'success': True,
            'message': 'Stats retrieved successfully',
            'data': {
                'view_count': view_count,
                'shortlist_count': shortlist_count
            }
        }), 200
    
    def display_fail(self, message="Failed to retrieve stats", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status

