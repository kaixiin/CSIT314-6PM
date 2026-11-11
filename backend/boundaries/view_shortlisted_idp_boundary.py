from flask import jsonify, session
from controllers.customer_controller import ViewShortlistedIDPC

class ViewShortlistedIDPPg:
    
    def view_favourite_list(self):

        account_id = session.get("account_id")
        
        if not account_id:
            return self.display_fail("Login required", 401)
        
        idps = ViewShortlistedIDPC().view_favourite_list(account_id)
        
        if idps is None:
            return self.display_fail("Error retrieving shortlisted IDPs")
        
        if len(idps) == 0:
            return self.display_results([])
        
        return self.display_results(idps)
    
    def display_results(self, idps):

        if len(idps) == 0:
            return jsonify({
                'success': True,
                'message': "You haven't shortlisted any projects yet",
                'count': 0,
                'data': []
            }), 200
        
        idps_data = [idp.to_dict() for idp in idps]
        
        return jsonify({
            'success': True,
            'message': f'Found {len(idps)} shortlisted project(s)',
            'count': len(idps),
            'data': idps_data
        }), 200
    
    def display_fail(self, message="Failed to retrieve shortlisted IDPs", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status
