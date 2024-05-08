from flask import Flask
from flask_migrate import Migrate
import os

from models import db, User, Parcel, Order, Profile

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['FLASK_SECRET_KEY'] = 'UVHUIJLKCVJVKJXLKV'

    migrate = Migrate(app, db)
    db.init_app(app)
    
    return app

app = create_app()

