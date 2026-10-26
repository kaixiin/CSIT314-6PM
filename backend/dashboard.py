from flask import request, jsonify
from flask.views import MethodView

#import controllers
from controllers.admin_controller import CreateUserProfile_C

class Dashboard(MethodView):
    # ─── GET DASHBOARD DISPLAY (GET) ───
    def get(self):
        """ Runs automatically when someone loads the dashboard page """
        account_type = request.cookies.get("account_type")
        
        #if account_type == "UserAdmin":
        #    # Admin sees server metrics, user counts, and flag lists
        #    data = GetAdminDashboardData_C().execute()
        #    return jsonify({"role": "Admin", "dashboard_data": data}), 200
            
        return jsonify({"message": "Unauthorized"}), 403


    # ─── BUTTON FUNCTION (POST) ───
    # The Matrix: Maps [Account Type] -> [Allowed URL Actions] -> [User Story Controller]
    CONTROLLER_MATRIX = {
        "UserAdmin": {
            "create_user_profile": CreateUserProfile_C,
            #"suspend_account": SuspendAccount_C
        }
    }

    def post(self, action_name):
        # 1. Get the account type from the secure login cookie
        account_type = request.cookies.get("account_type")
        
        # 2. Get the allowed actions dictionary for this specific role
        allowed_actions = self.CONTROLLER_MATRIX.get(account_type)
        if not allowed_actions:
            return jsonify({"status": "error", "message": "Unauthorized role context"}), 403

        # 3. Security Check: Is this specific user story controller allowed for this role?
        controller_class = allowed_actions.get(action_name)
        if not controller_class:
            return jsonify({
                "status": "error", 
                "message": f"Your role ({account_type}) is not authorized to perform action: {action_name}"
            }), 403

        # 4. Instantiate the user story controller dynamically and execute it
        active_controller = controller_class()
        payload = request.get_json() or {}
        
        is_success = active_controller.execute(payload)
        
        if is_success:
            return jsonify({"status": "success", "message": f"User story '{action_name}' completed."}), 200
        return jsonify({"status": "error", "message": "Execution failed."}), 400
