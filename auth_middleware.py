from functools import wraps
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

# Custom decorator to check if the user is an admin or super admin
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_data = get_jwt_identity()
        current_user_id = current_user_data.get('userId')
        
        current_user = User.query.filter_by(id=current_user_id).first()
        if current_user and not current_user.is_admin:
            return make_response(jsonify({"msg": "Admin access required"})), 403
        return fn(*args, **kwargs)
    return wrapper