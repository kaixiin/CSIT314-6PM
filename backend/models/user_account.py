# Entity: UserAccount
# Methods:
#   verify_login(username:str, password:str): UserAccount
#   logout(): void
#   check_existing(username:str, email:str): bool
#   create_user_account(profile_id:int, username:str, email:str, password:str): UserAccount

from extensions import db
from models.user_profile import UserProfile
from flask import session

class UserAccount(db.Model):
    __tablename__ = "user_account" 
    account_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("user_profile.profile_id"), nullable=False)
    profile = db.relationship("UserProfile")
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_suspended = db.Column(db.Boolean, default=False)

    @staticmethod
    def find_by_username(username):
        """Return account with this username, or None."""
        return UserAccount.query.filter_by(username=username).first()

    def check_password(self, password):
        """True if the password matches. Plain-text compare for now."""
        return self.password == password

    @staticmethod
    def verify_login(username, password):
        """Return matching UserAccount, or None if the login fails."""
        account = UserAccount.find_by_username(username)
        if account is None or account.is_suspended:
            return None
        if not account.check_password(password):
            return None
        return account

    @staticmethod
    def logout():
        """End the current session."""
        session.clear()

    def to_dict(self):
        """Safe to send to the page. Never includes the password."""
        return {
            "account_id": self.account_id,
            "username": self.username,
            "email": self.email,
            "profile_id": self.profile_id,
            "is_suspended": self.is_suspended,
        }

    @staticmethod
    def check_existing(username, email):
        """True if the username or the email is already used."""
        query = UserAccount.query.filter(
            db.or_(
                db.func.lower(UserAccount.username) == username.lower(),
                db.func.lower(UserAccount.email) == email.lower(),
            )
        )
        return db.session.query(query.exists()).scalar()

    def to_dict(self):
        """Safe to send to the page. Never includes the password."""
        return {
            "account_id": self.account_id,
            "username": self.username,
            "email": self.email,
            "profile_id": self.profile_id,
            "is_suspended": self.is_suspended,
        }

    @staticmethod
    def check_existing(username, exclude_account_id=None):
        """True if another account already uses this username."""
        query = UserAccount.query.filter(
            db.func.lower(UserAccount.username) == username.lower())
        if exclude_account_id is not None:
            query = query.filter(UserAccount.account_id != exclude_account_id)
        return db.session.query(query.exists()).scalar()

    @classmethod
    def create_user_account(cls, username, password, email, profile_id):
        """True if created. False if the profile is missing, the username/email is taken, or saving fails."""
        if db.session.get(UserProfile, profile_id) is None or cls.check_existing(username):
            return False
        try:
            db.session.add(cls(username=username, password=password,
                               email=email, profile_id=profile_id))
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"create_user_account failed: {e}")
            return False

    @staticmethod
    def view_user_account(account_id):
        """Return the account, or None."""
        return db.session.get(UserAccount, account_id)

    @classmethod
    def update_user_account(cls, account_id, username, email, profile_id):
        account = db.session.get(cls, account_id)
        if (account is None or db.session.get(UserProfile, profile_id) is None
                or cls.check_existing(username, exclude_account_id=account_id)):
            return False
        try:
            account.username = username
            account.email = email
            account.profile_id = profile_id
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"update_user_account failed: {e}")
            return False

    @classmethod
    def suspend_user_account(cls, account_id):
        account = db.session.get(cls, account_id)
        if account is None:
            return False
        try:
            account.is_suspended = True
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"suspend_user_account failed: {e}")
            return False

    @staticmethod
    def search_user_account(keyword):
        """Partial, case-insensitive match on the username. Empty keyword returns all."""
        return (UserAccount.query
                .filter(UserAccount.username.ilike(f"%{keyword}%"))
                .order_by(UserAccount.username)
                .all())