# CSIT314-6PM

## Backend setup

1. Create the database: run `backend/database/schema.sql` then `seed.sql` in MySQL Workbench
2. In `backend/`:
   ```
   python -m venv .venv
   .venv\Scripts\activate.bat
   python -m pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your MySQL password
4. Run `python app.py`