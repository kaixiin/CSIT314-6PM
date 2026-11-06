# Entity: UserProfile
# Used by: Create user profile (User Admin)
# Methods:

from extensions import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    account_type = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    is_suspended = db.Column(db.Boolean, default=False)

    # -- STATIC METHODS -- UTILITY FUNCTIONS --
    @staticmethod
    def check_existing(account_type):
        account_type = account_type

        return db.session.query(
            UserProfile.query.filter_by(account_type=account_type).exists()).scalar()

    # -- CLASS METHODS -- APP LOGIC --
    #CREATE USER PROFILE - #3
    @classmethod
    def create_user_profile(cls, name, account_type, description): 

        if cls.check_existing(account_type):
            return None

        else:
            try:
                new_profile = cls(name=name, account_type=account_type, description = description)
                db.session.add(new_profile)
                db.session.commit()
                return new_profile

            except IntegrityError as e:
                db.session.rollback()
                print(f"Database Integrity Error: {e.orig}")
                return False

            except Exception as e:
                db.session.rollback()
                print(f"An unexpected error occurred: {e}")
                return False

    #VIEW ALL USER PROFILES
    @classmethod
    def view_all_user_profiles(cls): 

        try:
            all_profiles = db.session.query(cls).order_by(cls.profile_id).all()
            return all_profiles
            
        except Exception as e:
            print(f"Error fetching user profiles: {e}")
            return None 

    #VIEW USER PROFILE - #4 (#126)
    @classmethod
    def view_user_profile(cls, profile_id): 
            
            try:
                profile = db.session.get(cls, profile_id)
                return profile
                
            except Exception as e:
                print(f"Error fetching user profiles: {e}")
                return None 

    #UPDATE USER PROFILE - #5 (#127)
    @classmethod
    def update_user_profile(cls, profile_id, name=None, account_type=None, description=None): 
            
        try:
            profile = db.session.get(profile_id)

            if profile is None:
                return None

            if account_type is not None:
                if account_type != profile.account_type:
                    exist = cls.check_existing(account_type)
                    if exist:
                        return False
                profile.account_type = account_type
                profile.name = name

            if description is not None:
                profile.description = description

            db.session.commit()
            return True
      
        except IntegrityError as e:
            db.session.rollback()
            print(f"Database Integrity Error: {e.orig}")
            return False
    
        except Exception as e:
            db.session.rollback()
            print(f"An unexpected error occurred: {e}")
            return False

    #SUSPEND USER PROFILE - #6 (#128)
    @classmethod
    def suspend_user_profile(cls, profile_id, is_suspended=True): 
            
        try:
            profile = db.session.get(cls, profile_id)

            if profile is None:
                return None

            profile.is_suspended = is_suspended

            db.session.commit()
            return True
    
        except Exception as e:
            db.session.rollback()
            print(f"Error setting suspension status: {e}")
            return False    

    #SEARCH USER PROFILE - #7
    @classmethod
    def search_user_profiles(cls, keyword):
        try:
            search_term = f"%{keyword}%"

            profiles = db.session.query(cls).filter(
                or_(
                    cls.name.ilike(search_term),
                    cls.account_type.ilike(search_term),
                    cls.description.ilike(search_term)
                )
            ).order_by(cls.profile_id).all()

            return profiles

        except Exception as e:
            print(f"Error searching user profiles: {e}")
            return None