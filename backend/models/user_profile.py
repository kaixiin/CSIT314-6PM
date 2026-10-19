# Entity: UserProfile
# Used by: Create user profile (User Admin)
# Methods:

from extensions import db


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    account_type = db.Column(
        db.Enum("UserAdmin", "InteriorDesigner", "Customer", "PlatformManager"),
        nullable=False,
    )
    is_suspended = db.Column(db.Boolean, default=False)