# Test setup and teardown for the unit tests.
# Each test gets its own throwaway MySQL database, so real data and seed.sql are never touched.
#
# Run from the backend folder:  pytest -v

import os
import sys

import mysql.connector
import pytest
from dotenv import load_dotenv

BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND)
load_dotenv(os.path.join(BACKEND, ".env"))

# Must be set before config.py is imported, because Config reads DB_NAME once
TEST_DB = "csit314_test"
os.environ["DB_NAME"] = TEST_DB

from app import create_app
from extensions import db
from models.user_account import UserAccount
from models.user_profile import UserProfile

ACTIVE_EMAIL = "active.user@test.local"
SUSPENDED_EMAIL = "suspended.user@test.local"
CORRECT_PASSWORD = "Correct-Pass-1"
WRONG_PASSWORD = "Wrong-Pass-1"


def run_sql(sql):
    conn = mysql.connector.connect(
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD", ""),
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "3306")),
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


@pytest.fixture
def login_accounts():
    # Setup: an empty database with one active account and one suspended account
    run_sql(f"DROP DATABASE IF EXISTS {TEST_DB}")
    run_sql(f"CREATE DATABASE {TEST_DB}")
    app = create_app()
    with app.app_context():
        db.create_all()
        profile = UserProfile(name="Test Role", account_type="TestRole", description="Used by the tests")
        db.session.add(profile)
        db.session.flush()
        db.session.add_all([
            UserAccount(profile_id=profile.profile_id, username="active_user",
                        email=ACTIVE_EMAIL, password=CORRECT_PASSWORD),
            UserAccount(profile_id=profile.profile_id, username="suspended_user",
                        email=SUSPENDED_EMAIL, password=CORRECT_PASSWORD, is_suspended=True),
        ])
        db.session.commit()
        yield
        db.session.remove()
        db.engine.dispose()
    # Teardown: nothing from the test is left behind
    run_sql(f"DROP DATABASE IF EXISTS {TEST_DB}")
