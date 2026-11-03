"""
Separated db in individual file so the import direction does not loop
app.py -> boundary -> controllers -> entities -> extensions.py

App connects to db later in create_app() with db.init_app(app)
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()