import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy.sql import text

# 1. Load the variables from the .env file
load_dotenv()

app = Flask(__name__)

# 2. Safely extract variables using os.environ.get()
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT', '3306') # Defaults to 3306 if not found
db_name = os.environ.get('DB_NAME')

# 3. Construct the secure URI string dynamically
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Connected securely without exposing passwords!"

if __name__ == '__main__':
    app.run(debug=True)