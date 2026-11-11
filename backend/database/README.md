# Database

| File | What it is |
|---|---|
| `schema.sql` | Creates the database and all tables |
| `seed.sql` | Fixed test data used in our test cases (the logins below) |
| `scripts/generate_user_data.py` | Bulk test data: 180 extra user accounts |
| `scripts/generate_idp_data.py` | Bulk test data: 100 companies, 100 IDPs, categories, favourites and views |

## 1. Create the database

In MySQL Workbench, run `schema.sql`, then `seed.sql`.

To start over, run `DROP DATABASE interior_design_platform;` first. This deletes all data.

Seed logins:

| Username | Password | Profile |
|---|---|---|
| admin01 | admin123 | User Admin |
| id01 | id123 | Interior Designer |
| cust01 | cust123 | Customer |
| pm01 | pm123 | Platform Manager |

## 2. Generate bulk test data

Run from the `backend/` folder with the venv active, using `-m` and no `.py`:

```
cd backend
.venv\Scripts\activate
python -m database.scripts.generate_user_data
```

In Git Bash, activate with `source .venv/Scripts/activate` instead.

This adds 180 accounts spread over the 4 seed profiles (all with password `password123`):

| Usernames | Profile | Count |
|---|---|---|
| admin001 – admin005 | User Admin | 5 |
| designer001 – designer120 | Interior Designer | 120 |
| customer001 – customer050 | Customer | 50 |
| manager001 – manager005 | Platform Manager | 5 |

Every 12th account is suspended (15 in total), for testing suspended logins.

- **Safe to re-run:** it removes the accounts it made last time before inserting them again.
- **Never touches the seed data:** generated accounts all have emails ending in `@test123.com`. Don't change this domain in the script, and never set it to `test.com` (the seed accounts' domain), or the clean-up step will delete the wrong accounts.
- if anything fails, no changes are saved.

### Categories, companies, IDPs, favourites and views

Run this after `generate_user_data`, because every row belongs to a generated account:

```
python -m database.scripts.generate_idp_data
```

| Table | Rows | Details |
|---|---|---|
| `idp_category` | 90 more (100 with the seed) | Property types, styles, rooms, services and commercial spaces; every 15th is suspended |
| `company_profile` | 100 | One each for the first 100 active designers, with trade-style names and addresses; the other designers have no company, for testing that screen |
| `idp` | 100 | Two each for the first 50 of those designers, about 70% `Past` and 30% `Current`, in active categories only. Titles, descriptions and budgets match each project's category |
| `favourite` | About 200 | 3 to 6 per active customer |
| `idp_view` | About 1,600 | One before every favourite, plus 3 to 25 more per IDP from active customers |

- IDP `created_at`, favourite `saved_at` and `viewed_at` are spread over the last 180 days, for the reports. Nothing is dated before its IDP, and every favourite has a view before it.
- The same data comes out on every run. Only the dates move, because they count back from today.
- **Safe to re-run:** it removes its own rows first, and seed data is never touched.
- To remove these rows only: `python -m database.scripts.generate_idp_data --clear`. A generated category that something real now uses is kept.
- To get back to the seed data, run that first, then `generate_user_data --clear`.
- Running `generate_user_data` again deletes this data too, because it recreates the accounts. Run this script again afterwards.
- `user_profile` stays at the 4 roles from `seed.sql`. Every other table has about 100 records or more.
- `idp.images` and `company_profile.logo` are left empty, since uploaded files are stored per computer.

To remove the generated accounts and all test data linked to them:

```
python -m database.scripts.generate_user_data --clear
```

### Common errors

| Error | Fix |
|---|---|
| `No module named 'config'` | You ran it from the wrong folder or without `-m`. `cd backend` and use `python -m database.scripts.generate_user_data` |
| `No module named 'sqlalchemy'` | The venv isn't active. Activate it first |
| `Missing base profiles` | Run `seed.sql` first |
| `Table ... doesn't exist` | Your database is older than `schema.sql`. Run the missing `CREATE TABLE` blocks and their `INSERT` statements |
| `No active IDP categories` | Run the `idp_category` `INSERT` from `seed.sql` first |
| `Not enough generated accounts` | Run `generate_user_data` first |
| `Unknown column 'image'` or `'images'` | Your database is older than `schema.sql`. Run `ALTER TABLE idp DROP COLUMN image, ADD COLUMN images JSON;` |
