from flask import Blueprint
from flask_restful import Api
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from models import User, Parcel, Order, Profile

serializer_bp = Blueprint('serializer_bp', __name__)
ma = Marshmallow(serializer_bp)
api = Api(serializer_bp)

class ParcelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Parcel
        include_fk = True

parcel = ParcelSchema()

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
    
    parcel = Nested(ParcelSchema, many=True)

orderSchema = OrderSchema()

class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True

profileSchema = ProfileSchema()

class UserSchema(SQLAlchemyAutoSchema):
    
    class Meta:
        model = User
        include_fk = True
        exclude = ('password',)
    
    parcel = Nested(ParcelSchema, many=True)
    profile = Nested(ProfileSchema, many=True)

userSchema = UserSchema()