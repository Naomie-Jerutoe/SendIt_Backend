from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

# Custom decorator to check if the user is an admin or super admin
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        if current_user.is_admin != True :
            return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper