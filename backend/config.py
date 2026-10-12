import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# 1. Load variables from .env file
load_dotenv()

class Config:
  # 2. Safely extract variables using os.environ.get()
  db_user = os.environ.get('DB_USER')
  db_password = quote_plus(os.environ.get('DB_PASSWORD','')) #Fix 1: encode symbols like @ # /
  db_host = os.environ.get('DB_HOST', 'localhost')
  db_port = os.environ.get('DB_PORT', '3306') # Defaults to 3306 if not found
  db_name = os.environ.get('DB_NAME')

  # 3. Construct the secure URI string dynamically
  SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  