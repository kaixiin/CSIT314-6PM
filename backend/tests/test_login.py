# Unit tests for login: UserLoginC.verify_login(email, password)
# The test data goes in through the code instead of being typed into the login page.
# verify_login returns the matching UserAccount, or None if the login fails.

# dblogintest must come first: it points the app at the test database
from dblogintest import ACTIVE_EMAIL, CORRECT_PASSWORD, SUSPENDED_EMAIL, WRONG_PASSWORD, login_accounts
from controllers.user_login_controller import UserLoginC


# Positive testing: correct email and correct password
def test_login_with_correct_email_and_password(login_accounts):
    account = UserLoginC().verify_login(ACTIVE_EMAIL, CORRECT_PASSWORD)
    assert account is not None
    assert account.email == ACTIVE_EMAIL


# Negative testing: correct email but wrong password
def test_login_with_wrong_password(login_accounts):
    account = UserLoginC().verify_login(ACTIVE_EMAIL, WRONG_PASSWORD)
    assert account is None


# Negative testing: email that does not belong to any account
def test_login_with_unknown_email(login_accounts):
    account = UserLoginC().verify_login("nobody@test.local", CORRECT_PASSWORD)
    assert account is None


# Negative testing: correct details, but the account is suspended
def test_login_with_suspended_account(login_accounts):
    account = UserLoginC().verify_login(SUSPENDED_EMAIL, CORRECT_PASSWORD)
    assert account is None
