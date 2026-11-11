# ID VIEW IDP CATEGORY
# Boundary: ViewCategoriesPg
# Methods: view_categories(), display_result(categories), display_fail(message)

from flask import jsonify, session
from controllers.id_controller import ViewCategoriesC

class ViewCategoriesPg:
    
    def view_categories(self):
       
        account_id = session.get("account_id")
        
        if not account_id:
            return self.display_fail("Login required", 401)
        
        categories = ViewCategoriesC().get_all_categories()
        
        if categories is None:
            return self.display_fail("Error retrieving categories")
        
        if len(categories) == 0:
            return jsonify({
                'success': True,
                'message': 'No categories found',
                'data': []
            }), 200
        
        return self.display_result(categories)
    
    def display_result(self, categories):

        categories_data = [category.to_dict() for category in categories]
        
        return jsonify({
            'success': True,
            'message': f'Found {len(categories)} category(ies)',
            'data': categories_data
        }), 200
    
    def display_fail(self, message="Failed to retrieve categories", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status
