from functools import wraps
from flask import jsonify, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from models import User

# Custom decorator to check if the user is an admin or super admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('is_admin'):
            return fn(*args, **kwargs)
        else:
            return make_response(jsonify({"message": "Admin access required"}), 403)
    return wrapper



