from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from models import db, User
from flask_jwt_extended import  jwt_required
from schemas import userSchema

user_bp = Blueprint('user_bp', __name__)
ma = Marshmallow(user_bp)
api = Api(user_bp)

class Users(Resource):
  @jwt_required()
  def get(self):
    users = User.query.all()
    result = userSchema.dump(users, many=True)
    return make_response(jsonify(result), 200)

api.add_resource(Users, '/users')

class UserById(Resource):
  def get(self, id):
    user = User.query.filter_by(id=id).first()
    result = userSchema.dump(user)
    return make_response(jsonify(result),200)

api.add_resource(UserById, '/users/<string:id>')    
    
    