from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.sql import text
from config import Config
from extensions import db
from routes.auth_routes import auth_bp  #registered for Login/Logout authentication 
from routes.useradmin_routes import admin_bp  #registered for Admin functions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"]
    }
    })
    
    #register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    #db health check route
    @app.route('/')
    def index():
        count = db.session.execute(text('SELECT COUNT(*) FROM user_profile')).scalar()
        return jsonify(status='ok', user_profiles=count)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
