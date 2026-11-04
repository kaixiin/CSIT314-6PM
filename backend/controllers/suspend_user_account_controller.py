# Controller: SuspendUserAccountC
# Methods:
#   suspend_user_account(account_id:int, is_suspended:bool): bool

from models.user_account import UserAccount


class SuspendUserAccountC:
    def suspend_user_account(self, account_id, is_suspended=True):
        return UserAccount.suspend_user_account(account_id, is_suspended)
