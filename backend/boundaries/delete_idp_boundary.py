# DELETE IDP (PAST + CURRENT) - #23, 28
# Boundary: DeleteIDPPg
# Methods:
#   delete_idp(): calls DeleteIDPC, then deletes specified IDP from DB  
# Calls: DeleteIDPC.delete_idp() in controllers/id_controller.py
from flask import jsonify, session
from controllers.id_controller import DeleteIDPC

class DeleteIDPPg:
    
    def delete_idp(self, idp_id):
    
        account_id = session.get("account_id")
        
        if not account_id:
            return self.display_fail("Login required", 401)
        
        is_deleted = DeleteIDPC().delete_idp(idp_id, account_id)
        
        if is_deleted is None:
            return self.display_fail(f'IDP with ID {idp_id} not found', 404)
        
        if is_deleted is False:
            return self.display_fail('Failed to delete IDP. You may not have permission.', 403)
        
        return self.display_success()
    
    def display_success(self):
        return jsonify({
            'success': True,
            'message': 'IDP deleted successfully'
        }), 200
    
    def display_fail(self, message="Delete IDP Failed", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status
