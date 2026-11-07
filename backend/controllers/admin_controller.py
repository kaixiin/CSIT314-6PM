from models.user_profile import UserProfile
from models.user_account import UserAccount
# USER PROFILE
# -----------------------------------------
# CREATE UP - #3
# Controller: CreateUserProfileC
# Methods:
#   create_user_profile(self, name,account_type, description)
# Calls: UserProfile.create_user_profile() in models/user_profile.py

class CreateUserProfileC:

    def create_user_profile(self, name, account_type, description):
        new_profile = UserProfile.create_user_profile(name, account_type, description)
        
        return new_profile

# -----------------------------------------
# Controller: ViewAllUserProfileC
# Methods:
#   view_all_user_profiles()
# Calls: UserProfile.view_all_user_profiles() in models/user_profile.py
 
class ViewAllUserProfileC:
    def view_all_user_profiles(self):
        return UserProfile.view_all_user_profiles()

# -----------------------------------------
# VIEW UP - #4(#126)
# Controller: ViewUserProfileC
# Methods:
#   view_user_profile()
# Calls: UserProfile.view_user_profile() in models/user_profile.py
 
class ViewUserProfileC:
    def view_user_profile(self, profile_id):
        profile = UserProfile.view_user_profile(profile_id)

        return profile

# -----------------------------------------
# UPDATE UP - #5(#127)
# Controller: UpdateUserProfileC
# Methods:
#   update_user_profile()
# Calls: UserProfile.update_user_profile() in models/user_profile.py
 
class UpdateUserProfileC:
    def update_user_profile(cls, profile_id, name=None, account_type=None, description=None): 
        return UserProfile.update_user_profile(profile_id, name, account_type, description)

# -----------------------------------------
# SUSPEND UP - #6(#128)
# Controller: SuspendUserProfileC
# Methods:
#   suspend_user_profile()
# Calls: UserProfile.suspend_user_profile() in models/user_profile.py
 
class SuspendUserProfileC:
    def suspend_user_profile(cls, profile_id, is_suspended): 
        return UserProfile.suspend_user_profile(profile_id, is_suspended)

# -----------------------------------------
# SEARCH UP - #7
# Controller: SearchUserProfile
# Methods:
#   search_user_profiles()
# Calls: UserProfile.search_user_profiles() in models/user_profile.py
 
class SearchUserProfileC:
    def search_user_profiles(cls, keyword): 
        return UserProfile.search_user_profiles(keyword)

#USER ACCOUNT
# -----------------------------------------
# CREATE UA - #8
# Controller: CreateUserAccountC
# Methods:
#   create_user_account(username:str, password:str, email:str, profile_id:int): bool
# Calls: UserAccount.create_user_account() in models/user_account.py

class CreateUserAccountC:
    def create_user_account(self, username, password, email, profile_id):
        return UserAccount.create_user_account(username, password, email, profile_id)

# -----------------------------------------
# Controller: ViewAllUserProfileC
# Methods:
#   view_all_user_profiles()
# Calls: UserProfile.view_all_user_profiles() in models/user_profile.py
 
class ViewAllUserProfileC:
    def view_all_user_profiles(self):
        return UserProfile.view_all_user_profiles()

# -----------------------------------------
# VIEW UA - #9 + VIEW ALL UAs
# Controller: ViewUserAccountC
# Methods:
#   view_user_account(account_id:int): UserAccount

class ViewUserAccountC:
    def view_user_account(self, account_id):
        return UserAccount.view_user_account(account_id)
    
# -----------------------------------------
# UPDATE UA - #10
# Controller: UpdateUserAccountC
# Methods:
#   update_user_account(account_id:int, username:str, email:str, profile_id:int): bool

class UpdateUserAccountC:
    def update_user_account(self, account_id, username, email, profile_id):
        return UserAccount.update_user_account(account_id, username, email, profile_id)

# -----------------------------------------
# SUSPEND UA - #11
# Controller: SuspendUserAccountC
# Methods:
#   suspend_user_account(account_id:int, is_suspended:bool): bool

class SuspendUserAccountC:
    def suspend_user_account(self, account_id, is_suspended=True):
        return UserAccount.suspend_user_account(account_id, is_suspended)
    
# -----------------------------------------
# SEARCH UA - #12
# Controller: SearchUserAccountC
# Methods:
#   search_user_account(keyword:str): List[UserAccount]

class SearchUserAccountC:
    def search_user_account(self, keyword):
        return UserAccount.search_user_account(keyword)


