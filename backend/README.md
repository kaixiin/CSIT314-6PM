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

## Project structure
Each feature follows the BCE diagrams: one entity (model), one controller and one route file.
```
backend/
  app.py            creates the Flask app and registers the routes
  config.py         settings loaded from .env
  extensions.py     shared objects (db)
  models/           Entity layer: classes that read/write the database tables
  controllers/      Controller layer: one file per controller, calls the models
  routes/           API endpoints the frontend calls, calls the controllers
  database/         schema.sql and seed.sql
```

### Adding a new feature
1. Add or extend a model in `models/` (e.g. `user_account.py`).
2. Add controller in `controllers/` named after the BCE class (e.g. `user_login_controller.py`).
3. Add the endpoints in `routes/` and register them in `app.py`.

### Naming
- Keep method names and parameters the same as in the sequence, BCE and UML diagrams.