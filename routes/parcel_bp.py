from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Parcel, User, db
from flask_restful import Api, Resource

parcel_bp = Blueprint('parcel_bp', __name__)
api = Api(parcel_bp)

# Route 1: Create parcel order with a parcel ID
# @parcel_bp.route('/parcels', methods=['POST'])
# @jwt_required
# def create_parcel():
#     user_id = get_jwt_identity()
#     data = request.get_json()
#     new_parcel = Parcel(user_id=user_id, **data)
#     db.session.add(new_parcel)
#     db.session.commit()
#     return jsonify({"message": "Hooray! Your parcel order has been created successfully!", "parcel": new_parcel.__repr__()}), 201

@parcel_bp.route('/parcels', methods=['POST'])
@jwt_required
def create_parcel():
    user_id = get_jwt_identity()
    # user_id = request.args.get('user_id')
    data = request.get_json()
    pickup_location = data.get('pickup_location')
    destination = data.get('destination')
    weight = data.get('weight')
    price = data.get('price')
    description = data.get('description')
    
    new_parcel = Parcel(
      user_id=user_id, 
      pickup_location = pickup_location,
      destination = destination,
      weight = weight,
      price = price,
      description = description
    )
    db.session.add(new_parcel)
    db.session.commit()

    return make_response(jsonify({"message": "Hooray! Your parcel order has been created successfully!"}), 201)

# Route 2: Get details of a parcel order by parcel ID
@parcel_bp.route('/parcels/<int:parcel_id>', methods=['GET'])
@jwt_required

def get_parcel(parcel_id):
    parcel = Parcel.query.get(parcel_id)
    if parcel:
        return jsonify({"message": "Great! We found your parcel details!", "parcel": parcel.__repr__()}), 200
    else:
        return jsonify({"message": "Oops! We couldn't find a parcel with that ID."}), 404

# Route 3: Change destination of a specific parcel delivery order
@parcel_bp.route('/parcels/<int:parcel_id>/destination', methods=['PUT'])
@jwt_required
def change_destination(parcel_id):
    user_id = get_jwt_identity()
    parcel = Parcel.query.get(parcel_id)
    if parcel and parcel.user_id == user_id and parcel.status != 'delivered':
        data = request.get_json()
        parcel.destination = data.get('destination')
        db.session.commit()
        return jsonify({"message": "Destination updated successfully! Your parcel is on its way to the new destination.", "parcel": parcel.__repr__()}), 200
    else:
        return jsonify({"message": "Sorry, we can't change the destination of this parcel."}), 400

# # Route 4: Cancel a specific parcel delivery order
@parcel_bp.route('/parcels/<int:parcel_id>/cancel', methods=['PUT'])
@jwt_required
def cancel_parcel(parcel_id):
    user_id = get_jwt_identity()
    parcel = Parcel.query.get(parcel_id)
    if parcel and parcel.user_id == user_id and parcel.status != 'delivered':
        parcel.status = 'cancelled'
        db.session.commit()
        return jsonify({"message": "Parcel cancelled successfully! We've halted delivery for this parcel.", "parcel": parcel.__repr__()}), 200
    else:
        return jsonify({"message": "Sorry, we can't cancel this parcel."}), 400

# # Route 5: Get a list of all parcel deliveries associated to a user
@parcel_bp.route('/users/<int:user_id>/parcels', methods=['GET'])
@jwt_required
def get_user_parcels(user_id):
    parcels = Parcel.query.filter_by(user_id=user_id).all()
    return jsonify({"message": "Here are all the parcels associated with this user!", "parcels": [parcel.__repr__() for parcel in parcels]}), 200

# # Route 6: List all the parcels (requires admin access)
@parcel_bp.route('/parcels', methods=['GET'])
@jwt_required
def get_all_parcels():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.is_admin:
        parcels = Parcel.query.all()
        return jsonify({"message": "As an admin, you have access to all parcels. Here they are!", "parcels": [parcel.__repr__() for parcel in parcels]}), 200
    else:
        return jsonify({"message": "Unauthorized access. Only admins can view all parcels."}), 403
