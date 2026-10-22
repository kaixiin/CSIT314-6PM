# Controller: CreateUserProfile_C
# Methods:
#   create_userProfile(self, name, account_type)
# Calls: UserProfile.create_user_profile() in models/user_profile.py
        

from models.user_profile import UserProfile

class CreateUserProfile_C:

    def execute(self, data):
        
        profile_name = data.get("name")
        account_type = data.get("account_type")
        return UserProfile.create_user_profile(profile_name, account_type) 
        