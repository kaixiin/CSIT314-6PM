# Entity: UserProfile
# Used by: Create user profile (User Admin)
# Methods:

from extensions import db
from sqlalchemy.exc import IntegrityError


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    account_type = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    is_suspended = db.Column(db.Boolean, default=False)

    @staticmethod
    def check_existing(account_type):
        account_type = account_type

        return db.session.query(
            UserProfile.query.filter_by(account_type=account_type).exists()).scalar()

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


