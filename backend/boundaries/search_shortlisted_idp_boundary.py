# SEARCH SHORTLISTED IDP - #36
# Boundary: SearchShortlistedIDPPg
# Methods: search_favourites(account_id, keyword), display_results(idps_data), display_fail(message)

from flask import jsonify, session
from controllers.customer_controller import SearchShortlistedIDPC

class SearchShortlistedIDPPg:
    
    def search_favourites(self, keyword):
        
        account_id = session.get("account_id")
        
        if not account_id:
            return self.display_fail("Login required", 401)
        
        if not keyword or not keyword.strip():
            return self.display_fail("Search keyword cannot be empty")
        
        keyword = keyword.strip()
        
        idps = SearchShortlistedIDPC().search_favourite(account_id, keyword)
        
        if idps is None:
            return self.display_fail("Error searching shortlisted IDPs")
        
        if len(idps) == 0:
            return self.display_results([], f'No matches found for "{keyword}" in your shortlist')
        
        return self.display_results(idps, f'Search results for "{keyword}": {len(idps)} project(s)')
    
    def display_results(self, idps, message):
       
        idps_data = [idp.to_dict() for idp in idps] if idps else []
        
        return jsonify({
            'success': True,
            'message': message,
            'count': len(idps),
            'data': idps_data
        }), 200
    
    def display_fail(self, message="Search failed", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status
