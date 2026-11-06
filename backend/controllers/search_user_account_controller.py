# Controller: SearchUserAccountC
# Methods:
#   search_user_account(keyword:str): List[UserAccount]

from models.user_account import UserAccount


class SearchUserAccountC:
    def search_user_account(self, keyword):
        return UserAccount.search_user_account(keyword)