#ID SEARCH IDP (PAST + CURRENT) - #24, 29
# Boundary: IDSearchIDPPg
# Methods:
#  id_search_idp(): calls IDSearchIDPC, then returns specified IDP from DB  
# Calls: IDSearchIDP.id_search_idp() in controllers/id_controller.py

from flask import jsonify, session, request
from controllers.id_controller import IDSearchIDPC

class IDSearchIDPPg:
    
    def search_my_idp(self):
    
        account_id = session.get("account_id")
        
        if not account_id:
            return jsonify({
                'success': False,
                'message': 'Login required'
            }), 401
        
        keyword = request.args.get("q", "").strip()
        status = request.args.get("status", "").strip()
        
        if status and status not in ["Current", "Past"]:
            return jsonify({
                'success': False,
                'message': 'Status must be "Current" or "Past"'
            }), 200
        
        idps = IDSearchIDPC().search_my_idp(account_id, keyword, status if status else None)
        
        if idps is None:
            return jsonify({
                'success': False,
                'message': 'Error searching IDPs'
            }), 200
        
        if len(idps) == 0:
            filters = []
            if keyword:
                filters.append(f'keyword "{keyword}"')
            if status:
                filters.append(f'status "{status}"')
            
            message = f'No IDPs found' + (f' matching {" and ".join(filters)}' if filters else '')
            
            return jsonify({
                'success': True,
                'message': message,
                'data': []
            }), 200
        
        idps_data = [idp.to_dict() for idp in idps]
        
        return jsonify({
            'success': True,
            'message': f'Found {len(idps)} IDP(s)',
            'data': idps_data
        }), 200
