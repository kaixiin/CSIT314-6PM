# Controller: CreateUserProfile_C
# Methods:
#   create_userProfile(self, name)
# Calls: UserProfile.create_user_profile() in models/user_profile.py
        

from models.user_profile import UserProfile

class CreateUserProfileC:

    def create_user_profile(self, name, account_type, description):
        new_profile = UserProfile.create_user_profile(name, account_type, description)
        
        return new_profile