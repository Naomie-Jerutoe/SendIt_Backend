from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from routes.user_bp import user_bp
import os

from models import db, User, Parcel, Order, Profile

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_database_he6p_user:7dCWh8gZ2f6V2YieOfn1mgS4b9wfx7vo@dpg-coh5e0v79t8c73fsrohg-a.oregon-postgres.render.com/send_it_db'
    app.config['FLASK_SECRET_KEY'] = 'UVHUIJLKCVJVKJXLKV'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    

    migrate = Migrate(app, db)
    db.init_app(app)
    JWTManager(app)
    CORS(app)

    return app

app = create_app()
