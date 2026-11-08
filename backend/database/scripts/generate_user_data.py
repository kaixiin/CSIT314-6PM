# Generates bulk test data for user accounts. See database/README.md.

import sys

from sqlalchemy import create_engine, text

from config import Config

GEN_EMAIL_DOMAIN = "test123.com"
PASSWORD = "password123"

# How many accounts to create for each existing role (account_type from seed.sql)
ACCOUNTS_PER_ROLE = {
    "UserAdmin": ("admin", 5),
    "InteriorDesigner": ("designer", 120),  # enough active designers for 100 companies
    "Customer": ("customer", 50),
    "PlatformManager": ("manager", 5),
}
SUSPENDED_EVERY = 12  # every 12th generated account is suspended


def clear_generated(conn):
    """Delete only accounts this script created, and anything that points to them."""
    pattern = {"pattern": f"%@{GEN_EMAIL_DOMAIN}"}
    generated = "SELECT account_id FROM user_account WHERE email LIKE :pattern"
    # Children first, or the foreign keys block the delete
    for table in ("idp_view", "favourite", "idp", "company_profile"):
        conn.execute(text(f"DELETE FROM {table} WHERE account_id IN ({generated})"), pattern)
    accounts = conn.execute(text("DELETE FROM user_account WHERE email LIKE :pattern"), pattern).rowcount
    print(f"Removed {accounts} previously generated accounts and their test data")


def insert_accounts(conn):
    profile_ids = dict(conn.execute(text("SELECT account_type, profile_id FROM user_profile")).all())
    missing = [t for t in ACCOUNTS_PER_ROLE if t not in profile_ids]
    if missing:
        sys.exit(f"Missing base profiles {missing}: run seed.sql first.")

    count = 0
    for account_type, (prefix, how_many) in ACCOUNTS_PER_ROLE.items():
        for n in range(1, how_many + 1):
            count += 1
            username = f"{prefix}{n:03d}"  # e.g. designer017
            conn.execute(text(
                "INSERT INTO user_account (profile_id, username, password, email, is_suspended) "
                "VALUES (:p, :u, :pw, :e, :s)"),
                {"p": profile_ids[account_type], "u": username, "pw": PASSWORD,
                 "e": f"{username}@{GEN_EMAIL_DOMAIN}", "s": count % SUSPENDED_EVERY == 0})
    print(f"Inserted {count} user accounts ({count // SUSPENDED_EVERY} suspended)")


if __name__ == "__main__":
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.begin() as conn:  # if anything fails, nothing is saved
        clear_generated(conn)
        if "--clear" not in sys.argv:
            insert_accounts(conn)

        total = conn.execute(text("SELECT COUNT(*) FROM user_account")).scalar()
        print(f"  user_account: {total} rows")
