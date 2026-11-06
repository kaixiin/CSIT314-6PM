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
Each user story follows the BCE diagrams: route → boundary → controller → entity.
```
backend/
  app.py            creates the Flask app and registers the routes
  config.py         settings loaded from .env
  extensions.py     shared objects (db)
  routes/           API endpoints the frontend calls; one blueprint per role, calls the boundaries
  boundaries/       Boundary layer: one file per user story, checks input and builds the response
  controllers/      Controller layer: one file per user story, passes values to the entity
  models/           Entity layer: classes that read/write the database tables
<<<<<<< HEAD
  database/         schema.sql and seed.sql

frontend/
  index.html        all screens, one section per role
  css/style.css
  js/core/          shared, loads first:
    config.js         backend address (API_CONFIG.BASE_URL)
    state.js          shared data and role mapping
    api.js            loads data from the backend
    ui.js             rendering, dialogs and the view router show()
  js/auth/          login.js, logout.js
  js/admin/         User Admin: profile.js, account.js       (/api/admin)
  js/id/            Interior Designer: company.js            (/api/id)
  js/customer/      Customer                                 (/api/customer)
  js/pm/            Platform Manager                         (/api/pm)
=======
  controllers/      Controller layer: one file per controller, calls the models
  routes/           API endpoints the frontend calls, calls the controllers
  database/         schema.sql, seed.sql and test data scripts (see database/README.md)
>>>>>>> origin/company-profile
```
New frontend files go in their role's folder and get a `<script>` tag in `index.html`, after `core/`.

### Adding a new feature
1. Add or extend a model in `models/` (e.g. `user_account.py`).
2. Add a controller class in `controllers/` (e.g. `CreateUserProfileC` in `admin_controller.py`).
3. Add a boundary in `boundaries/` named after the user story (e.g. `create_user_profile_boundary.py`).
4. Add the route to the role's blueprint in `routes/` (and register new blueprints in `app.py`).

### Naming
- Keep method names and parameters the same as in the sequence, BCE and UML diagrams.