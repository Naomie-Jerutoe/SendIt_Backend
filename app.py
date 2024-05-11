from routes.parcel_bp import parcel_bp
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from routes.user_bp import user_bp
import os
from routes.courier_bp import profile_bp

from models import db, User, Parcel, Order, Profile, TokenBlocklist
from routes.courier_bp import profile_bp

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['FLASK_SECRET_KEY'] = 'UVHUIJLKCVJVKJXLKV'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    
    #Register the blueprint
    app.register_blueprint(parcel_bp)


    migrate = Migrate(app, db)
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    
    app.register_blueprint(profile_bp)
    
    return app

app = create_app()