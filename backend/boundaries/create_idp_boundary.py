from flask import jsonify, session
from boundaries.idp import read_idp_form, remove_idp_images
from controllers.id_controller import CreateIDPC

class CreateIDPPg:
    def create_idp(self, data):
        fields, error = read_idp_form(data)
        if error:
            return self.display_fail(error)

        new_idp = CreateIDPC().create_idp(
            session["account_id"],
            fields["category_id"],
            fields["title"],
            fields["description"],
            fields["location"],
            fields["budget"],
            fields["status"],
            fields["images"]  
        )
        
        if not new_idp:
            # remove saved uploaded images if create fails
            remove_idp_images(fields["images"])  
            return self.display_fail("Create Interior Design Project failed.")
            
        return self.display_success(new_idp)

    def display_success(self, new_idp):
        return jsonify({
            "success": True,
            "profile": new_idp.to_dict()
        }), 201

    def display_fail(self, message, status=400):
        return jsonify({
            "success": False,
            "message": message
        }), status
