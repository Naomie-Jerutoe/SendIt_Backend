from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String())
  is_admin = db.Column(db.Boolean, default=False)
  
  def __repr__(self):
        return f"<User {self.username}>"
  
class Parcel(db.Model):
  __tablename__ = 'parcels'
  
  id = db.Column(db.Integer, primary_key=True)
  pickup_location = db.Column(db.String)
  destination = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  weight = db.Column(db.Float, nullable=False)
  price = db.Column(db.Float, nullable=True)
  description = db.Column(db.String)
  
  users = db.relationship('User', backref='parcels')
  
  def __repr__(self):
        return f"<Parcel {self.description} ID: {self.id}>"
  
class Order(db.Model):
  __tablename__ = 'orders'
  
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(Enum('delivered', 'enroute', 'canceled'))
  parcel_id = db.Column(db.Integer, db.ForeignKey('parcels.id'))

  parcels = db.relationship('Parcel', backref='orders')
  
  def __repr__(self):
        return f"<Order {self.status}, {self.parcel_id} >"

class Profile(db.Model):
  __tablename__ = 'profiles'
  
  id = db.Column(db.Integer, primary_key=True)
  profile_picture = db.Column(db.String(255))
  location = db.Column(db.String)
  created_at = db.Column(db.DateTime, default=db.func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
  users = db.relationship('User', backref='profiles')
  
  def __repr__(self):
        return f"<Profile {self.user_id}>"

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=db.func.now())
    
    def __repr__(self):
        return f"<Token {self.jti}>"


