from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, User, Parcel
from datetime import datetime

users_bp = Blueprint('users', __name__)
bcrypt = Bcrypt()

@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        email=data['email'],
        username=data['username'],
        is_admin=False,
        password=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User already exists'}), 400

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'userId': user.id, 'is_admin': user.is_admin, 'username': user.username})
        return jsonify({'token': access_token, 'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'The credentials you provided are incorrect'}), 400


@users_bp.route('/users/<int:user_id>/makeadmin', methods=['PATCH'])
@jwt_required()
def make_user_admin(user_id):
    current_user = get_jwt_identity()
    if current_user['is_admin']:
        user = User.query.get(user_id)
        if user:
            user.is_admin = True
            db.session.commit()
            return jsonify({'message': 'The user has been made an admin successfully'}), 200
        else:
            return jsonify({'message': 'No such user'}), 204
    else:
        return jsonify({'message': 'Only admins can access this route'}), 403
