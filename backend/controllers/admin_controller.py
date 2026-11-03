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
    def view_all_user_profiles():
        return UserProfile.view_all_user_profiles()