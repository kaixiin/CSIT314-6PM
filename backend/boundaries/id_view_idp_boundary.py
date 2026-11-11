#ID VIEW IDP (PAST + CURRENT) - #21, 26
# Boundary: IDViewIDPPg
# Methods:
#   id_view_idp(): calls IDViewIDPC, then returns specified IDP from DB  
# Calls: IDViewIDP.id_view_idp() in controllers/id_controller.py

from flask import jsonify, session
from controllers.id_controller import IDViewIDPC

class IDViewIDPPg:
    def id_view_idp(self, idp_id):
        
        account_id = session.get("account_id")
        
        if not account_id:
            return self.display_fail("Login required", 401)
        
        idp = IDViewIDPC().id_view_idp(idp_id, account_id)
        
        if idp is None:
            return self.display_fail(f'IDP with ID {idp_id} not found', 404)
        
        return self.display_idp(idp)

    def display_idp(self, idp):
        return jsonify({
            "success": True,
            "profile": idp.to_dict()
        }), 200

    def display_fail(self, message="View IDP Failed", status=400):
        return jsonify({
                        'success': False,
                        'message': message
        }), status