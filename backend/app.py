from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.sql import text
from config import Config
from extensions import db
from routes.auth_routes import auth_bp  #registered for Login/Logout authentication
from routes.useradmin_routes import admin_bp  #registered for Admin functions
from routes.user_account_routes import user_account_bp  #registered for User Account functions
from routes.id_routes import id_bp
from routes.company_routes import id_bp          # adds the company routes to id_bp
from routes.logo_routes import logo_bp
from routes.pm_routes import pm_bp
from routes.customer_routes import cust_bp
import routes.report_routes
import routes.idp_category_routes     

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
    app.register_blueprint(user_account_bp)
    app.register_blueprint(id_bp)
    app.register_blueprint(logo_bp)
    app.register_blueprint(pm_bp)
    app.register_blueprint(cust_bp)

    #db health check route
    @app.route('/')
    def index():
        count = db.session.execute(text('SELECT COUNT(*) FROM user_profile')).scalar()
        return jsonify(status='ok', user_profiles=count)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
