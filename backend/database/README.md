# Database

| File | What it is |
|---|---|
| `schema.sql` | Creates the database and all tables |
| `seed.sql` | Fixed test data used in our test cases (the logins below) |
| `scripts/generate_user_data.py` | Bulk test data: 100 extra user accounts |

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

This adds 100 accounts spread over the 4 seed profiles (all with password `password123`):

| Usernames | Profile | Count |
|---|---|---|
| admin001 – admin005 | User Admin | 5 |
| designer001 – designer040 | Interior Designer | 40 |
| customer001 – customer050 | Customer | 50 |
| manager001 – manager005 | Platform Manager | 5 |

Every 12th account is suspended (8 in total), for testing suspended logins.

- **Safe to re-run:** it removes the accounts it made last time before inserting them again.
- **Never touches the seed data:** generated accounts all have emails ending in `@test123.com`. Don't change this domain in the script, and never set it to `test.com` (the seed accounts' domain), or the clean-up step will delete the wrong accounts.
- if anything fails, no changes are saved.

To remove the generated accounts only:

```
python -m database.scripts.generate_user_data --clear
```

### Common errors

| Error | Fix |
|---|---|
| `No module named 'config'` | You ran it from the wrong folder or without `-m`. `cd backend` and use `python -m database.scripts.generate_user_data` |
| `No module named 'sqlalchemy'` | The venv isn't active. Activate it first |
| `Missing base profiles` | Run `seed.sql` first |
