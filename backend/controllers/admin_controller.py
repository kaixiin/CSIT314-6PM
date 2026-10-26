# Controller: CreateUserProfile_C
# Methods:
#   create_userProfile(self, name)
# Calls: UserProfile.create_user_profile() in models/user_profile.py
        

from models.user_profile import UserProfile

class CreateUserProfile_C:

    def execute(self, data):
        
        profile_name = data.get("name")
        return UserProfile.create_user_profile(profile_name) 
        