# VIEW IDP AS CUSTOMER - #33
# Boundary:CustViewIDPPg
# Methods: view_idp(data), display_idp(idp), display_fail(message, status)

from flask import jsonify, session
from controllers.customer_controller import CustViewIDPC

class CustViewIDPPg:
    def view_idp(self, idp_id):

        account_id = session.get("account_id")

        if not account_id:
            return self.display_fail("Login required", 401)

        idp, recorded = CustViewIDPC().view_idp(idp_id, account_id)

        if idp is None:
            return self.display_fail(f'IDP with ID {idp_id} not found', 404)

        if not recorded:
            return self.display_fail('Failed to track view. Please try again.', 500)

        return self.display_idp(idp)

    def display_idp(self, idp):
        return jsonify({
            'success': True,
            'message': 'IDP retrieved successfully',
            'data': idp.to_dict()
        }), 200

    def display_fail(self, message="View IDP Failed", status=400):
        return jsonify({
            'success': False,
            'message': message
        }), status
