# Entity: UserAccount
# Methods:
#   verify_login(username:str, password:str): UserAccount
#   logout(): void

from extensions import db

class UserAccount(db.Model):
    __tablename__ = "user_account" 
    account_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, nullable=False)
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