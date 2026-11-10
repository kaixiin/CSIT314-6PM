# SEACRH IDP AS CUSTOMER - #32
# Boundary:CustSearchIDPPg
# Methods: search_idp(data), display_success(), display_fail(message, status)

from flask import jsonify, request
from controllers.customer_controller import CustSearchIDPC

class CustSearchIDPPg:
    
    def search_idp(self):

        keyword = request.args.get("q", "").strip()
        category_id_str = request.args.get("category_id", "").strip()
        
        category_id = None
        if category_id_str:
            try:
                category_id = int(category_id_str)
                if category_id < 1:
                    return jsonify({
                        'success': False,
                        'message': 'Invalid category ID'
                    }), 200
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Category ID must be a number'
                }), 200

        idps = CustSearchIDPC().search_idp(keyword, category_id)
        
        if idps is None:
            return jsonify({
                'success': False,
                'message': 'Error searching IDPs'
            }), 200
        
        if len(idps) == 0:
            filters = []
            if keyword:
                filters.append(f'keyword "{keyword}"')
            if category_id:
                filters.append(f'category ID {category_id}')
            
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
