from routes.parcel_bp import parcel_bp
from routes.user_bp import user_bp
from routes.courier_bp import profile_bp
from routes.order_bp import orders_bp
from login import users_bp
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from extensions import mail

from models import db, User, Parcel, Order, Profile, TokenBlocklist

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['DEBUG'] = True
    app.config['FLASK_SECRET_KEY'] = 'UVHUIJLKCVJVKJXLKV'
    app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    
    #Flask-mail configs
    app.config['MAIL_SERVER']= "smtp.gmail.com"
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "senditapp.cci@gmail.com"
    app.config['MAIL_PASSWORD'] = "gymw hsth ogdp hcrk"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    
    mail.init_app(app)

    migrate = Migrate(app, db)
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    
    @app.route('/')
    def index():
        return '<h1>Welcome to SendIt App</h1>'
    
    #Register the blueprint
    app.register_blueprint(parcel_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(orders_bp)
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

