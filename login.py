from flask import Blueprint, request, jsonify, render_template, make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, User, TokenBlocklist
from auth_middleware import admin_required
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask_restful import Api, Resource

users_bp = Blueprint('users', __name__)
bcrypt = Bcrypt()
api = Api(users_bp)

# Secret key used for token generation
SECRET_KEY = "NTo*|JRcOJ$)gT-"
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Store reset tokens and their associated users in a dictionary
reset_tokens = {}

# @users_bp.route('/signup', methods=['POST'])
class SignUpResource(Resource):   
    def post(self):
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
            return make_response(jsonify({'message': 'User registered successfully'}), 200)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'User already exists'}), 400)
        
api.add_resource(SignUpResource, '/signup')

# @users_bp.route('/login', methods=['POST'])
class SignInResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'userId': user.id, 'is_admin': user.is_admin, 'username': user.username})
            return make_response(jsonify({'token': access_token, 'message': 'Login successful'}), 200)
        else:
            return make_response(jsonify({'message': 'The credentials you provided are incorrect'}), 400)
api.add_resource(SignInResource, '/login')


# @users_bp.route('/makeadmin', methods=['GET'])
class MakeAdmin(Resource):
    @admin_required
    def get(self):
        return make_response(jsonify({'message': 'Admin registered successfully'}))

api.add_resource(MakeAdmin, '/makeadmin')

# @users_bp.route('/logout', methods=['GET'])
class LogoutResource(Resource):
    @jwt_required()
    def get(self):
        current_user_data = get_jwt_identity()
        token = get_jwt()
        blocked_token = TokenBlocklist(
            jti=token['jti'], created_at=datetime.utcnow())
        db.session.add(blocked_token)
        db.session.commit()
        return make_response(jsonify({'detail': "Logged out Successfully"}), 200)

api.add_resource(LogoutResource, '/logout')

# @users_bp.route('/upgradeuser', methods=['POST'])
class UpgradeUser(Resource):
    @admin_required
    def post(self):
        data = request.get_json()

        if 'userId' not in data:
            return make_response(jsonify({'error': 'Missing userId field'}), 400)

        user_id = data['userId']
        user = User.query.get(user_id)

        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)

        user.is_admin = True
        db.session.commit()

        return make_response(jsonify({'message': 'User upgraded to admin successfully'}), 200)

api.add_resource(UpgradeUser, '/upgrade_user')

# @users_bp.route('/forgotpassword', methods=['POST'])
class ForgotPassword(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        if not email:
            return make_response(jsonify({'error': 'Missing email field'}), 400)

        user = User.query.filter_by(email=email).first()
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)

        # Generate a unique reset token
        token = serializer.dumps(email, salt='reset-password')

        # Store the token and user ID in reset_tokens
        reset_tokens[token] = user.id

        # Render a template with the token to be displayed to the user
        return render_template('reset_password.html', token=token)

api.add_resource(ForgotPassword, '/forgot_password')

# @users_bp.route('/resetpassword', methods=['POST'])
class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')

        if not token or not new_password:
            return make_response(jsonify({'error': 'Missing token or password field'}), 400)

        # Verify if the token is valid and not expired
        try:
            email = serializer.loads(token, salt='reset-password', max_age=3600)
        except:
            return make_response(jsonify({'error': 'Invalid or expired token'}), 400)

        user_id = reset_tokens.get(token)
        if not user_id:
            return make_response(jsonify({'error': 'Invalid token'}), 400)

        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)

        # Update the user's password
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        # Remove the token from the reset_tokens dictionary
        del reset_tokens[token]

        return make_response(jsonify({'message': 'Password reset successfully'}), 200)

api.add_resource(ResetPassword, '/resetpassword')

