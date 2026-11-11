# Generates bulk test data for categories, companies, IDPs, favourites and views.
# See database/README.md.
# Run generate_user_data first: every row here belongs to a generated account.

import random
import sys
from datetime import datetime, timedelta

from sqlalchemy import create_engine, text

from config import Config

GEN_EMAIL_DOMAIN = "test123.com"
HOW_MANY_COMPANIES = 100  # the remaining designers stay without a company
HOW_MANY_IDPS = 100
DESIGNERS_WITH_IDPS = 50  # so each of these designers has more than one IDP to search
GEN_CATEGORY_NOTE = "Generated test category"   # older runs marked their categories with this
GEN_PROFILE_TYPE = "GeneratedType"   # older runs made these; user_profile should only hold the 4 seed roles
SUSPENDED_CATEGORY_EVERY = 15
FAVOURITES_PER_CUSTOMER = (3, 6)   # lowest and highest
VIEWS_PER_IDP = (3, 25)   # on top of one view before every favourite
PAST_DAYS = 180           # dates are spread over this many days, for the reports
RANDOM_SEED = 314         # the same data comes out on every run and every machine

# ---- Categories: (name, description), in 5 groups ----
PROPERTY_TYPES = [
    ("HDB 2-Room Flexi", "Compact two-room flats, often for singles and retirees."),
    ("HDB 3-Room", "Three-room HDB flats, from new BTOs to older resale units."),
    ("HDB 4-Room", "Four-room HDB flats, the most common family home."),
    ("HDB 5-Room", "Five-room HDB flats with space for a larger family."),
    ("HDB Executive Apartment", "Executive flats with an extra study or utility room."),
    ("HDB Executive Maisonette", "Two-storey executive maisonettes."),
    ("BTO", "New Build-To-Order flats renovated from bare finishes."),
    ("Resale HDB", "Older HDB flats, often with hacking and rewiring."),
    ("Condominium", "Private condominium apartments."),
    ("Executive Condominium", "Executive condominiums (ECs)."),
    ("Penthouse", "Top-floor penthouses and duplex units."),
    ("Studio Apartment", "Studio and one-bedroom apartments."),
    ("Walk-up Apartment", "Low-rise walk-up apartments."),
    ("Terrace House", "Intermediate and corner terrace houses."),
    ("Semi-Detached House", "Semi-detached landed homes."),
    ("Bungalow", "Detached bungalows."),
    ("Cluster House", "Cluster and strata landed homes."),
    ("Shophouse", "Conserved shophouses used as homes or businesses."),
]
STYLES = [
    ("Scandinavian", "light woods, white walls and simple forms"),
    ("Japandi", "a calm mix of Japanese and Scandinavian design"),
    ("Minimalist", "clean lines and hidden storage"),
    ("Modern Contemporary", "neutral colours and current, versatile finishes"),
    ("Industrial", "exposed brick, concrete and black metal"),
    ("Mid-Century Modern", "1950s and 60s shapes with warm wood"),
    ("Modern Luxe", "marble, brass and rich textures"),
    ("Wabi-Sabi", "raw textures and imperfect, natural finishes"),
    ("Muji", "warm wood and plain, practical design"),
    ("Bohemian", "layered patterns, plants and rattan"),
    ("Tropical", "open, airy spaces and natural materials"),
    ("Peranakan", "heritage tiles, colour and carved details"),
    ("Modern Colonial", "black and white walls, timber and shutters"),
    ("Farmhouse", "rustic wood and relaxed country details"),
    ("Art Deco", "bold geometric patterns and gold accents"),
    ("Rustic", "weathered wood and earthy tones"),
    ("Coastal", "whites, blues and light, breezy fabrics"),
    ("Eclectic", "a personal mix of styles and eras"),
    ("Korean Minimalist", "soft neutrals and rounded furniture"),
    ("Vintage Retro", "terrazzo, bright colours and nostalgic pieces"),
]
ROOMS = [
    ("Living Room", "built a TV feature wall with hidden storage and reworked the seating layout"),
    ("Kitchen", "replaced the cabinets, added a quartz countertop and moved the fridge for a better work triangle"),
    ("Master Bedroom", "built a full-height wardrobe and a headboard wall with reading lights"),
    ("Children's Bedroom", "added a loft bed with a study desk underneath and plenty of toy storage"),
    ("Bathroom", "retiled the walls and floor, redid the waterproofing and fitted a frameless shower screen"),
    ("Walk-in Wardrobe", "turned a small bedroom into a walk-in wardrobe with open shelving and a dressing table"),
    ("Study", "built a long desk along the window with bookshelves above"),
    ("Home Office", "set up a quiet work corner with a built-in desk, cable management and good lighting"),
    ("Dining Room", "added a bench seat with storage underneath and a pendant light over the table"),
    ("Balcony", "laid outdoor decking and added built-in seating and planters"),
    ("Entryway and Foyer", "built a shoe cabinet with a bench and a full-length mirror"),
    ("Yard and Service Area", "fitted a laundry cabinet, a drying rack and storage for cleaning tools"),
    ("Laundry Area", "stacked the washer and dryer and added cabinets and a folding counter"),
    ("Home Bar", "built a bar counter with a wine fridge and glass shelves"),
    ("Rooftop Terrace", "added a pergola, an outdoor kitchen and lounge seating"),
]
SERVICES = [
    ("Full Home Renovation", "renovated the whole home, from hacking and rewiring to carpentry and painting"),
    ("Partial Renovation", "redid the kitchen and bathrooms while keeping the existing flooring"),
    ("Kitchen Remodelling", "rebuilt the kitchen with new cabinets, a quartz top and built-in appliances"),
    ("Bathroom Remodelling", "stripped both bathrooms back and redid the tiles, fittings and waterproofing"),
    ("Custom Carpentry", "built wardrobes, a TV console and kitchen cabinets to fit each space exactly"),
    ("False Ceiling and Lighting", "added a false ceiling with cove lighting and recessed downlights"),
    ("Flooring Replacement", "replaced the old tiles with vinyl flooring throughout"),
    ("Space Planning", "rearranged the layout so every room has a clear purpose"),
    ("Wall Hacking", "hacked a non-structural wall to join the kitchen and living room"),
    ("Painting", "repainted every room in warm neutral colours"),
    ("Smart Home", "installed smart lights, a digital lock and voice-controlled switches"),
    ("Built-in Storage", "added full-height storage, a platform bed with drawers and a shoe cabinet"),
    ("Feature Walls", "built fluted panel and limewash feature walls in the living and dining areas"),
    ("Window Treatments", "fitted day-and-night blinds and sheer curtains in every room"),
    ("Electrical Rewiring", "rewired the home and added power points where they were needed"),
    ("Waterproofing", "redid the waterproofing in the bathrooms and the yard"),
    ("Furniture Styling", "chose furniture, rugs and art to finish the home"),
]
COMMERCIAL = [
    ("Café", "Cafés and coffee bars."),
    ("Restaurant", "Restaurants and casual dining."),
    ("Bar and Lounge", "Bars, lounges and wine rooms."),
    ("Bakery", "Bakeries and dessert shops."),
    ("Boutique Hotel", "Small hotels and guest rooms."),
    ("Office Fit-Out", "Offices fitted out for a new tenant."),
    ("Co-working Space", "Shared offices and hot desks."),
    ("Retail Boutique", "Fashion and lifestyle shops."),
    ("Showroom", "Product and brand showrooms."),
    ("Beauty Salon", "Hair, nail and beauty salons."),
    ("Barbershop", "Barbershops and grooming studios."),
    ("Spa", "Spas and massage studios."),
    ("Gym and Fitness Studio", "Gyms, yoga and pilates studios."),
    ("Dental Clinic", "Dental practices."),
    ("Medical Clinic", "GP and specialist clinics."),
    ("Preschool", "Preschools and childcare centres."),
    ("Tuition Centre", "Tuition and enrichment centres."),
    ("Event Space", "Event and function venues."),
    ("Pop-up Store", "Short-term retail pop-ups."),
    ("Coffee Kiosk", "Takeaway coffee kiosks."),
]

# ---- Places ----
HOME_PLACES = [  # (town, street)
    ("Tampines", "Tampines St 81"), ("Punggol", "Edgefield Plains"), ("Bishan", "Bishan St 22"),
    ("Toa Payoh", "Lorong 1 Toa Payoh"), ("Jurong East", "Jurong East St 21"), ("Clementi", "Clementi Ave 4"),
    ("Sengkang", "Anchorvale Road"), ("Bukit Batok", "Bukit Batok West Ave 6"), ("Ang Mo Kio", "Ang Mo Kio Ave 3"),
    ("Woodlands", "Woodlands Drive 16"), ("Yishun", "Yishun Ring Road"), ("Bedok", "Bedok North Ave 1"),
    ("Queenstown", "Dawson Road"), ("Serangoon", "Serangoon North Ave 1"), ("Hougang", "Hougang Ave 7"),
    ("Pasir Ris", "Pasir Ris Drive 6"), ("Bukit Panjang", "Fajar Road"), ("Choa Chu Kang", "Teck Whye Lane"),
]
COMMERCIAL_PLACES = ["Tiong Bahru", "Tanjong Pagar", "Joo Chiat", "Kampong Glam", "Raffles Place",
                     "Orchard", "Novena", "Paya Lebar", "Katong", "Bugis", "Holland Village", "Dempsey"]
HOMES = ["4-Room HDB", "5-Room HDB", "3-Room HDB", "BTO", "Resale Flat", "Condo", "EC", "Terrace House"]
LANDED = {"Terrace House", "Semi-Detached House", "Bungalow", "Cluster House", "Shophouse"}
SMALL = {"HDB 2-Room Flexi", "HDB 3-Room", "Studio Apartment", "Walk-up Apartment", "3-Room HDB"}  # no third bedroom

# ---- Description parts ----
CLIENTS = [
    ("A young couple", "wanted a bright home that is easy to clean"),
    ("A family of four", "needed more storage and a kitchen they could cook in every day"),
    ("A retired couple", "wanted a simpler, safer home with fewer steps and better lighting"),
    ("A working professional", "wanted a quiet home with a proper place to work"),
    ("A multi-generational family", "needed room for the grandparents as well as two young children"),
    ("First-time home owners", "wanted a warm look on a careful budget"),
    ("A couple with a newborn", "wanted a safe, practical home that would grow with their child"),
]
HOME_WORKS = [
    "hacked the kitchen wall for an open layout", "laid vinyl flooring throughout",
    "built full-height wardrobes in the bedrooms", "added a false ceiling with cove lighting",
    "turned the third bedroom into a study", "redid both bathrooms with new tiles and fittings",
    "built a TV feature wall with hidden storage", "rewired the whole home",
    "added a breakfast counter", "built a shoe cabinet and bench at the entrance",
]
SHOP_WANTS = ["feels welcoming from the street", "matches their brand",
              "fits more people without feeling crowded", "is easy to keep clean during busy hours"]
SHOP_WORKS = [
    "planned the layout around how staff and customers move", "built a custom counter and display shelving",
    "chose durable, easy-to-clean finishes", "designed lighting that works in the day and the evening",
    "put their logo on a feature wall", "finished the fit-out in six weeks so they could open on time",
]

# ---- Companies ----
BRAND_WORDS = ["Blueprint", "Hearth", "Cornerstone", "Plank", "Grain", "Nest", "Arch", "Brickwork",
               "Openhouse", "Square Metre", "Homecraft", "Canvas", "Inside Out", "Northlight", "Atrium",
               "Dwell", "Habitat", "Timberline", "Keystone", "Lattice", "Mortar", "Threshold", "Woodgrain"]
SURNAMES = ["Tan", "Lim", "Wong", "Ng", "Koh", "Goh", "Chua", "Ong", "Teo", "Lee"]
FIRM_TYPES = ["Interiors", "Interior Design", "Design Studio", "Design & Build", "Renovation"]
SPECIALITIES = ["HDB renovations", "BTO and resale flats", "condominium and landed homes",
                "commercial fit-outs for cafés and offices", "small homes and clever storage"]
COMPANY_EXTRAS = [
    "We handle everything from space planning to carpentry and handover.",
    "Our own carpenters build most of our cabinetry.",
    "Each project keeps the same designer from the first meeting to handover.",
    "We give a fixed quotation before any work starts.",
]
OFFICE_STREETS = [  # where design firms usually rent space, with the postal code prefix
    ("Ubi Crescent", "408"), ("Ubi Avenue 1", "408"), ("Kaki Bukit Road 1", "415"),
    ("Toh Guan Road East", "608"), ("Defu Lane 10", "539"), ("Sin Ming Lane", "573"),
    ("Kallang Bahru", "339"), ("Eunos Avenue 7", "409"), ("Changi South Lane", "486"),
    ("Woodlands Loop", "738"), ("Tai Seng Street", "534"), ("Kaki Bukit Avenue 1", "417"),
]


def category_rows():
    """All 90 generated categories as (name, description, group)."""
    rows = [(n, d, "property") for n, d in PROPERTY_TYPES]
    rows += [(n, f"Projects in the {n} style: {d}.", "style") for n, d in STYLES]
    rows += [(n, f"Makeovers focused on the {n.lower()}.", "room") for n, _ in ROOMS]
    rows += [(n, f"Projects where the main work was {n.lower()}.", "service") for n, _ in SERVICES]
    rows += [(n, d, "commercial") for n, d in COMMERCIAL]
    return rows


def clear_generated(conn):
    """Delete only rows owned by generated accounts, children first."""
    accounts = "SELECT account_id FROM user_account WHERE email LIKE :pattern"
    pattern = {"pattern": f"%@{GEN_EMAIL_DOMAIN}"}
    views = conn.execute(text(f"DELETE FROM idp_view WHERE account_id IN ({accounts})"), pattern).rowcount
    favourites = conn.execute(text(f"DELETE FROM favourite WHERE account_id IN ({accounts})"), pattern).rowcount
    idps = conn.execute(text(f"DELETE FROM idp WHERE account_id IN ({accounts})"), pattern).rowcount
    companies = conn.execute(text(f"DELETE FROM company_profile WHERE account_id IN ({accounts})"), pattern).rowcount
    # Kept if something real now uses them; the INSERT IGNOREs below then skip those rows
    names = [name for name, _, _ in category_rows()]
    marks = ", ".join(f":n{i}" for i in range(len(names)))
    categories = conn.execute(text(
        f"DELETE FROM idp_category WHERE (description LIKE :note OR name IN ({marks})) "
        "AND category_id NOT IN (SELECT category_id FROM idp)"),
        {"note": f"{GEN_CATEGORY_NOTE}%", **{f"n{i}": n for i, n in enumerate(names)}}).rowcount
    # Removes leftovers from older runs of this script
    profiles = conn.execute(text(
        "DELETE FROM user_profile WHERE account_type LIKE :t "
        "AND profile_id NOT IN (SELECT profile_id FROM user_account)"),
        {"t": f"{GEN_PROFILE_TYPE}%"}).rowcount
    print(f"Removed {companies} companies, {idps} IDPs, {favourites} favourites, {views} views, "
          f"{categories} categories and {profiles} profiles from the last run")


def insert_categories(conn):
    rows = category_rows()
    for n, (name, description, _) in enumerate(rows, 1):
        conn.execute(text(
            "INSERT IGNORE INTO idp_category (name, description, is_suspended) VALUES (:n, :d, :s)"),
            {"n": name, "d": description, "s": n % SUSPENDED_CATEGORY_EVERY == 0})
    print(f"Inserted {len(rows)} categories")


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


def company_names(rng):
    names = [f"{w} {t}" for w in BRAND_WORDS for t in FIRM_TYPES]
    names += [f"{s} & Co {t}" for s in SURNAMES for t in FIRM_TYPES if "&" not in t]
    rng.shuffle(names)
    return [f"{n} Pte Ltd" if i % 3 == 0 else n for i, n in enumerate(names)]


def insert_companies(conn, rng, designers):
    for account_id, name in zip(designers, company_names(rng)):
        slug = "".join(ch for ch in name.lower().replace("pte ltd", "") if ch.isalnum())
        speciality = rng.choice(SPECIALITIES + [f"{rng.choice(STYLES)[0]} homes"])
        street, postal = rng.choice(OFFICE_STREETS)
        conn.execute(text(
            "INSERT INTO company_profile (account_id, company_name, description, address, contact_number, email) "
            "VALUES (:a, :n, :d, :addr, :c, :e)"),
            {"a": account_id, "n": name,
             "d": f"{name} is a Singapore interior design firm specialising in {speciality}. "
                  f"{rng.choice(COMPANY_EXTRAS)}",
             "addr": f"{rng.randint(1, 80)} {street}, #{rng.randint(1, 9):02d}-{rng.randint(1, 60):02d}, "
                     f"Singapore {postal}{rng.randint(100, 999)}",
             "c": f"6{rng.randint(1000000, 9999999)}", "e": f"{slug}@{GEN_EMAIL_DOMAIN}"})
    print(f"Inserted {len(designers)} companies")


def joined(items):
    return ", ".join(items[:-1]) + " and " + items[-1]


def home_works(rng, how_many, home):
    works = [w for w in HOME_WORKS if home not in SMALL or "third bedroom" not in w]
    return joined(rng.sample(works, how_many))


def home_story(rng, works):
    who, want = rng.choice(CLIENTS)
    return f"{who} {want}. We {works}."


def project_text(rng, name, group):
    """Title, description, location and budget that fit the category."""
    town, street = rng.choice(HOME_PLACES)
    home = rng.choice(HOMES)
    if group == "commercial":
        area = rng.choice(COMMERCIAL_PLACES)
        title = rng.choice([f"{name} Fit-Out at {area}", f"{area} {name}", f"New {name} in {area}"])
        desc = (f"The owners of a new {name.lower()} in {area} wanted a space that {rng.choice(SHOP_WANTS)}. "
                f"We {joined(rng.sample(SHOP_WORKS, 3))}.")
        return title, desc, f"{area}, Singapore", rng.randrange(30000, 300001, 1000)
    if group == "property":
        if name in LANDED:
            title = rng.choice([f"{town} {name}", f"{name} Renovation in {town}"])
            budget = rng.randrange(80000, 400001, 1000)
        else:
            title = rng.choice([f"{street} | {name}", f"{town} {name} Makeover", f"{name} in {town}"])
            budget = rng.randrange(20000, 60001, 500) if name in SMALL else rng.randrange(35000, 120001, 500)
        desc = home_story(rng, home_works(rng, 3, name))
    elif group == "style":
        title = rng.choice([f"{name} {home} in {town}", f"{town} {home} | {name}", f"A {name} Home in {town}"])
        desc = home_story(rng, home_works(rng, 2, home)) + f" The {name} look comes from {dict(STYLES)[name]}."
        budget = rng.randrange(25000, 70001, 500) if home in SMALL else rng.randrange(35000, 150001, 500)
    elif group == "room":
        title = rng.choice([f"{name} for a {town} {home}", f"{town} {home} | {name}", f"{name} Makeover in {town}"])
        desc = home_story(rng, dict(ROOMS)[name])
        budget = rng.randrange(3000, 40001, 500)
    else:
        title = rng.choice([f"{name} for a {town} {home}", f"{town} {home} | {name}"])
        desc = home_story(rng, dict(SERVICES)[name])
        budget = rng.randrange(3000, 90001, 500)
    return title, desc, f"{street}, Singapore", budget


def insert_idps(conn, rng, designers, now):
    groups = {name: group for name, _, group in category_rows()}
    categories = [(cid, name) for cid, name in conn.execute(text(
        "SELECT category_id, name FROM idp_category WHERE is_suspended = FALSE ORDER BY category_id")).all()
        if name in groups]
    if not categories:
        sys.exit("No active generated categories: check the categories step above.")

    for n in range(HOW_MANY_IDPS):
        category_id, name = rng.choice(categories)
        title, desc, location, budget = project_text(rng, name, groups[name])
        conn.execute(text(
            "INSERT INTO idp (account_id, category_id, title, description, location, budget, status, created_at) "
            "VALUES (:a, :c, :t, :d, :l, :b, :s, :at)"),
            {"a": designers[n % DESIGNERS_WITH_IDPS], "c": category_id, "t": title, "d": desc,
             "l": location, "b": budget,
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
            insert_categories(conn)
            insert_companies(conn, rng, designers)
            insert_idps(conn, rng, designers, now)
            insert_favourites(conn, rng, customers, now)
            insert_views(conn, rng, customers, now)

        for table in ("idp_category", "user_profile", "company_profile", "idp", "favourite", "idp_view"):
            total = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  {table}: {total} rows")
