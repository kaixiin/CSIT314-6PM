# Controller: UserLogoutC
# Methods:
#   logout()
# Calls: UserAccount.logout() in models/user_account.py

from models.user_account import UserAccount
class UserLogoutC:
    def logout(self):
        UserAccount.logout()