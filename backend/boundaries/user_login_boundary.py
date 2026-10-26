# Boundary: UserLoginPg
# Methods:
#   login(data): checks the input, calls UserLoginC, then shows success or fail
#   display_success(account)
#   display_fail()
# Calls: UserLoginC.verify_login() in controllers/user_login_controller.py

from flask import session, jsonify
from controllers.user_login_controller import UserLoginC

class UserLoginPg:
    def login(self, data):
        username = data.get("username") if isinstance(data, dict) else None
        password = data.get("password") if isinstance(data, dict) else None

        # input checks belong to the boundary
        if not isinstance(username, str) or not isinstance(password, str):
            return self.display_fail()
        username = username.strip()
        if not username or not password:
            return self.display_fail()

        account = UserLoginC().verify_login(username, password)
        if account is None:
            return self.display_fail()

        session.clear()
        session["account_id"] = account.account_id
        session["profile_id"] = account.profile_id
        session["account_type"] = account.profile.account_type
        return self.display_success(account)

    def display_success(self, account):
        profile = account.profile
        return jsonify({
            "success": True,
            "account": {
                "account_id": account.account_id,
                "username": account.username,
                "profile_id": account.profile_id,
                "account_type": profile.account_type
            },
        }), 200

    def display_fail(self):
        return jsonify({"success": False, "message": "Login failed"}), 401