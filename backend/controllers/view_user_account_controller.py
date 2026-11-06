# Controller: ViewUserAccountC
# Methods:
#   view_user_account(account_id:int): UserAccount

from models.user_account import UserAccount


class ViewUserAccountC:
    def view_user_account(self, account_id):
        return UserAccount.view_user_account(account_id)