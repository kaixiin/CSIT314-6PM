# CREATE IDP (PAST + PRESENT) - #20, 25
# Boundary: CreateIDPPg
# Methods:
#   create_idp(data): checks input, calls the controller, shows the result
#   display_success(IDP)
#   display_fail(message)

from flask import jsonify, session
from boundaries.idp import read_idp_form, remove_idp_images
from controllers.id_controller import CreateIDPC


class CreateIDPPg:
    def create_idp(self, data):
        fields, error = read_idp_form(data)
        if error:
            return self.display_fail(error)

        new_idp = CreateIDPC().create_idp(
            session["account_id"], fields["category_id"], fields["title"],
            fields["description"], fields["location"], fields["budget"], fields["status"], fields["image"])
        
        if not new_idp:
            remove_idp_images(fields["image"])
            return self.display_fail(
                "Create Interior Design Project failed.")
        return self.display_success(new_idp)

    def display_success(self, new_idp):
            return jsonify({
                "success": True,
                "profile": {
                    "account_id": new_idp.account_id,
                    "category_id": new_idp.category_id,
                    "title": new_idp.title,
                    "description":new_idp.description,
                    "location": new_idp.location,
                    "budget" : new_idp.budget,
                    "status" : new_idp.status,
                    "image" : new_idp.image
                }
            }), 201

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status