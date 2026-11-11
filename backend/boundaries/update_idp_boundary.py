#UPDATE IDP - #22, 27
# Boundary: UpdateIDPPg
# Methods:
#   update_idp(): checks input with validate_update then calls UpdateIDPC, then updates the details in the DB 
# Calls: UpdateIDPC.update_idp() in controllers/id_controller.py

from flask import jsonify
from controllers.id_controller import UpdateIDPC
from boundaries.idp import validate_update_idp_fields, remove_idp_images, new_photo_names

class UpdateIDPPg:
    def update_idp(self, idp_id, data):
        
        fields, error = validate_update_idp_fields(data)
        
        if error:
            return self.display_fail(error)
        
        is_updated = UpdateIDPC().update_idp(
            idp_id=idp_id,
            **fields  
        )
        
        if is_updated is None:
            # clean up any newly uploaded images if update failed
            if fields.get("images"):
                remove_idp_images(new_photo_names(fields["images"], data.get("images")))
            return self.display_fail(f'IDP with ID {idp_id} not found', 404)
        
        if is_updated is False:
            # clean up any newly uploaded images if update failed
            if fields.get("images"):
                remove_idp_images(new_photo_names(fields["images"], data.get("images")))
            return self.display_fail('Failed to update IDP. Database error occurred.')
        
        return self.display_success()

    def display_success(self):
        return jsonify({
            'success': True,
            'message': 'IDP updated successfully'
        }), 200
    
    def display_fail(self, message="Update IDP Failed", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status
