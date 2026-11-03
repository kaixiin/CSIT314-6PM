# Controller: UpdateUserAccountC
# Methods:
#   update_user_account(account_id:int, username:str, email:str, profile_id:int): bool

from models.user_account import UserAccount


class UpdateUserAccountC:
    def update_user_account(self, account_id, username, email, profile_id):
        return UserAccount.update_user_account(account_id, username, email, profile_id)