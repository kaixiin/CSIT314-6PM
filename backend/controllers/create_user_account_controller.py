# Controller: CreateUserAccountC
# Methods:
#   create_user_account(username:str, password:str, email:str, profile_id:int): bool
# Calls: UserAccount.create_user_account() in models/user_account.py

from models.user_account import UserAccount

class CreateUserAccountC:
    def create_user_account(self, username, password, email, profile_id):
        return UserAccount.create_user_account(username, password, email, profile_id)