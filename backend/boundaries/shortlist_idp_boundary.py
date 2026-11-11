# Boundary: ShortlistIDPPg
# Methods:
#   save_favourite(idp_id): finds account_id from logged in user and calls controller to save idp into user's shortlist
#   display_success(message)
#   display_fail(message)
from flask import jsonify, session
from controllers.customer_controller import ShortlistIDPC

class ShortlistIDPPg:
    
    def save_favourite(self, idp_id):
        account_id = session.get("account_id")
        
        if not account_id:
            return self.display_fail("Login required", 401)
        
        result = ShortlistIDPC().save_favourite(account_id, idp_id)
        
        if result is None:
            return self.display_fail("Failed to save favourite. IDP may not exist.")

        if result is True:
            return self.display_success("IDP added to shortlist")
        else:
            return self.display_success("IDP removed from shortlist")
    
    def display_success(self, message):
        return jsonify({
            'success': True,
            'message': message
        }), 200
    
    def display_fail(self, message="Save favourite failed", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status
