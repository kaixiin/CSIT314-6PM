# Controller: UserLoginC
# Methods:
#   verify_login(username:str, password:str): UserAccount
#   current_user(account_id:int): UserAccount
# Calls: UserAccount.verify_login() in models/user_account.py

from models.user_account import UserAccount

class UserLoginC:
    def verify_login(self, username, password):
        """Return the matching UserAccount, or None if the login fails."""
        return UserAccount.verify_login(username, password)

    def current_user(self, account_id):
        """Return the logged-in account, or None if it is missing or suspended."""
        return UserAccount.find_active(account_id)
