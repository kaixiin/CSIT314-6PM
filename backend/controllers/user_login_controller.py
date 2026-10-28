# Controller: UserLoginC
# Methods:
#   verify_login(username:str, password:str): UserAccount
# Calls: UserAccount.verify_login() in models/user_account.py

from models.user_account import UserAccount

class UserLoginC:
    def verify_login(self, username, password):
        """Return the matching UserAccount, or None if the login fails."""
        if not isinstance(username, str) or not isinstance(password, str):
            return None
        username = username.strip()
        if not username or not password:
            return None
        return UserAccount.verify_login(username, password)