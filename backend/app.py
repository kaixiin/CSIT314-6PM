from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.sql import text
from config import Config
from extensions import db
from routes.auth_routes import auth_bp   

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app) #Fix 2: lets front-end call API
    app.register_blueprint(auth_bp)
    #Fix 3: Run a query, if fail means connection is wrong
    @app.route('/')
    def index():
        count = db.session.execute(text('SELECT COUNT(*) FROM user_profile')).scalar()
        return jsonify(status='ok', user_profiles=count)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)