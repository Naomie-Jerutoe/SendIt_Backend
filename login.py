from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, User, TokenBlocklist
from auth_middleware import admin_required
from datetime import datetime

users_bp = Blueprint('users', __name__)
bcrypt = Bcrypt()

@users_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    
    
    if not email or '@' not in email or '.' not in email:
        return jsonify({"error": "Invalid email address."}), 400

    if not (6 <= len(password) <= 50):
        return jsonify({"error": "Password must be between 8 and 50 characters."}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        email=data['email'],
        username=data['username'],
        is_admin=data['is_admin'],
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


@users_bp.route('/makeadmin', methods=['GET'])
@admin_required
def make_admin():
    return jsonify({'message': 'Admin registered successfully'})


@users_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    current_user_data = get_jwt_identity()
    token = get_jwt()
    blocked_token = TokenBlocklist(
        jti=token['jti'], created_at=datetime.utcnow())
    db.session.add(blocked_token)
    db.session.commit()
    return jsonify({'detail': "Logged out Successfully"})