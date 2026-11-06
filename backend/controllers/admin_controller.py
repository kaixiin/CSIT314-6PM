from models.user_profile import UserProfile
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
    def suspend_user_profile(cls, profile_id): 
        return UserProfile.suspend_user_profile(profile_id)

