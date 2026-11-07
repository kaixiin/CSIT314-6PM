# Generates bulk test data for companies, IDPs, favourites and views. See database/README.md.
# Run generate_user_data first: every row here belongs to a generated account.

import random
import sys
from datetime import datetime, timedelta

from sqlalchemy import create_engine, text

from config import Config

GEN_EMAIL_DOMAIN = "test123.com"
HOW_MANY_COMPANIES = 30   # the remaining designers stay without a company
HOW_MANY_IDPS = 100
FAVOURITES_PER_CUSTOMER = (3, 6)   # lowest and highest
VIEWS_PER_IDP = (3, 25)   # on top of one view before every favourite
PAST_DAYS = 180           # dates are spread over this many days, for the reports
RANDOM_SEED = 314         # the same data comes out on every run and every machine

COMPANY_FIRST = ["Studio", "Atelier", "Maison", "Casa", "House of", "Nook", "Oak", "Haven", "Form", "Linea"]
COMPANY_SECOND = ["Lumen", "Terra", "Verde", "Nova", "Ember", "Solace", "Aster"]
PLACES = ["Tampines", "Bishan", "Orchard", "Tiong Bahru", "Punggol", "Jurong East",
          "Toa Payoh", "Bukit Timah", "Marine Parade", "Serangoon", "Holland Village", "Clementi"]
STYLES = ["Scandinavian", "Japandi", "Industrial", "Minimalist", "Mid-Century",
          "Contemporary", "Tropical", "Coastal", "Classic", "Rustic"]
SPACES = ["Living Room", "Kitchen", "Master Bedroom", "Study", "Lobby",
          "Dining Area", "Reception", "Studio Apartment", "Bathroom", "Lounge"]


def clear_generated(conn):
    """Delete only rows owned by generated accounts, children first."""
    accounts = "SELECT account_id FROM user_account WHERE email LIKE :pattern"
    pattern = {"pattern": f"%@{GEN_EMAIL_DOMAIN}"}
    views = conn.execute(text(f"DELETE FROM idp_view WHERE account_id IN ({accounts})"), pattern).rowcount
    favourites = conn.execute(text(f"DELETE FROM favourite WHERE account_id IN ({accounts})"), pattern).rowcount
    idps = conn.execute(text(f"DELETE FROM idp WHERE account_id IN ({accounts})"), pattern).rowcount
    companies = conn.execute(text(f"DELETE FROM company_profile WHERE account_id IN ({accounts})"), pattern).rowcount
    print(f"Removed {companies} companies, {idps} IDPs, {favourites} favourites and {views} views from the last run")


def active_accounts(conn, account_type):
    """Generated accounts of one role that are not suspended."""
    return list(conn.execute(text(
        "SELECT a.account_id FROM user_account a "
        "JOIN user_profile p ON p.profile_id = a.profile_id "
        "WHERE p.account_type = :t AND a.email LIKE :pattern AND a.is_suspended = FALSE "
        "ORDER BY a.account_id"),
        {"t": account_type, "pattern": f"%@{GEN_EMAIL_DOMAIN}"}).scalars())


def random_date(rng, now, earliest=None):
    """A random moment between earliest (default PAST_DAYS ago) and now."""
    start = earliest or now - timedelta(days=PAST_DAYS)
    return start + timedelta(seconds=rng.randint(0, int((now - start).total_seconds())))


def insert_companies(conn, rng, designers):
    names = [f"{first} {second}" for first in COMPANY_FIRST for second in COMPANY_SECOND]
    rng.shuffle(names)
    for account_id, name in zip(designers, names):
        slug = name.lower().replace(" ", "")
        conn.execute(text(
            "INSERT INTO company_profile (account_id, company_name, description, address, contact_number, email) "
            "VALUES (:a, :n, :d, :addr, :c, :e)"),
            {"a": account_id, "n": name,
             "d": f"{name} designs {rng.choice(STYLES).lower()} interiors for homes and businesses.",
             "addr": f"{rng.randint(1, 200)} {rng.choice(PLACES)} Road, Singapore",
             "c": f"6{rng.randint(1000000, 9999999)}", "e": f"{slug}@{GEN_EMAIL_DOMAIN}"})
    print(f"Inserted {len(designers)} companies")


def insert_idps(conn, rng, designers, now):
    categories = list(conn.execute(text(
        "SELECT category_id FROM idp_category WHERE is_suspended = FALSE ORDER BY category_id")).scalars())
    if not categories:
        sys.exit("No active IDP categories: run seed.sql first.")

    for n in range(HOW_MANY_IDPS):
        place, style, space = rng.choice(PLACES), rng.choice(STYLES), rng.choice(SPACES)
        conn.execute(text(
            "INSERT INTO idp (account_id, category_id, title, description, location, budget, status, created_at) "
            "VALUES (:a, :c, :t, :d, :l, :b, :s, :at)"),
            {"a": designers[n % len(designers)], "c": rng.choice(categories),
             "t": f"{style} {space} in {place}",
             "d": f"A {style.lower()} {space.lower()} designed around natural light and everyday use.",
             "l": f"{place}, Singapore", "b": rng.randrange(5000, 120001, 500),
             "s": rng.choices(["Past", "Current"], weights=[7, 3])[0],
             "at": random_date(rng, now)})
    print(f"Inserted {HOW_MANY_IDPS} IDPs")


def insert_favourites(conn, rng, customers, now):
    idps = conn.execute(text(
        "SELECT i.idp_id, i.created_at FROM idp i JOIN user_account a ON a.account_id = i.account_id "
        "WHERE a.email LIKE :pattern ORDER BY i.idp_id"), {"pattern": f"%@{GEN_EMAIL_DOMAIN}"}).all()
    count = 0
    for account_id in customers:
        # sample() never picks the same IDP twice, which the UNIQUE rule needs
        for idp_id, created_at in rng.sample(idps, rng.randint(*FAVOURITES_PER_CUSTOMER)):
            count += 1
            conn.execute(text(
                "INSERT INTO favourite (account_id, idp_id, saved_at) VALUES (:a, :i, :at)"),
                {"a": account_id, "i": idp_id, "at": random_date(rng, now, earliest=created_at)})
    print(f"Inserted {count} favourites")


def insert_views(conn, rng, customers, now):
    pattern = {"pattern": f"%@{GEN_EMAIL_DOMAIN}"}
    rows = []
    # A customer opens an IDP before saving it, so every favourite gets an earlier view
    for account_id, idp_id, saved_at, created_at in conn.execute(text(
            "SELECT f.account_id, f.idp_id, f.saved_at, i.created_at FROM favourite f "
            "JOIN idp i ON i.idp_id = f.idp_id JOIN user_account a ON a.account_id = f.account_id "
            "WHERE a.email LIKE :pattern ORDER BY f.favourite_id"), pattern).all():
        rows.append({"a": account_id, "i": idp_id, "at": random_date(rng, saved_at, earliest=created_at)})
    # Extra browsing; a customer may open the same IDP more than once
    for idp_id, created_at in conn.execute(text(
            "SELECT i.idp_id, i.created_at FROM idp i JOIN user_account a ON a.account_id = i.account_id "
            "WHERE a.email LIKE :pattern ORDER BY i.idp_id"), pattern).all():
        for _ in range(rng.randint(*VIEWS_PER_IDP)):
            rows.append({"a": rng.choice(customers), "i": idp_id, "at": random_date(rng, now, earliest=created_at)})
    conn.execute(text("INSERT INTO idp_view (account_id, idp_id, viewed_at) VALUES (:a, :i, :at)"), rows)
    print(f"Inserted {len(rows)} views")


if __name__ == "__main__":
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.begin() as conn:  # if anything fails, nothing is saved
        clear_generated(conn)
        if "--clear" not in sys.argv:
            rng = random.Random(RANDOM_SEED)
            now = datetime.now().replace(microsecond=0)
            designers = active_accounts(conn, "InteriorDesigner")[:HOW_MANY_COMPANIES]
            customers = active_accounts(conn, "Customer")
            if len(designers) < HOW_MANY_COMPANIES or not customers:
                sys.exit("Not enough generated accounts: run generate_user_data first.")
            insert_companies(conn, rng, designers)
            insert_idps(conn, rng, designers, now)
            insert_favourites(conn, rng, customers, now)
            insert_views(conn, rng, customers, now)

        for table in ("company_profile", "idp", "favourite", "idp_view"):
            total = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  {table}: {total} rows")
