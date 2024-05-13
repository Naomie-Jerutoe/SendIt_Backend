from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Parcel, User, db
from flask_restful import Api, Resource
from auth_middleware import admin_required

parcel_bp = Blueprint('parcel_bp', __name__)
api = Api(parcel_bp)

class ViewAndCreateParcel(Resource):
    @jwt_required()
    def get(self):
        user_info = get_jwt_identity()
        user_id = user_info.get('userId')  # Assuming 'userId' is the key for user ID in JWT payload
        if user_id is None:
            return make_response(jsonify({"message": "User ID not found in token."}), 403)
        
        user = User.query.get(user_id)
        if user is None:
            return make_response(jsonify({"message": "User not found."}), 404)
        
        if user.is_admin:
            parcels = Parcel.query.all()
            return make_response(jsonify({"message": "As an admin, you have access to all parcels. Here they are!", "parcels": [parcel.__repr__() for parcel in parcels]}), 200)
        else:
            return make_response(jsonify({"message": "Unauthorized access. Only admins can view all parcels."}), 403)
    
    @jwt_required()
    def post(self):
        user_info = get_jwt_identity()
        user_id = user_info['userId']

        data = request.get_json()
        pickup_location = data.get('pickup_location')
        destination = data.get('destination')
        weight = data.get('weight')
        price = data.get('price')
        description = data.get('description')

        new_parcel = Parcel(
            user_id=user_id, 
            pickup_location=pickup_location,
            destination=destination,
            weight=weight,
            price=price,
            description=description
        )
        db.session.add(new_parcel)
        db.session.commit()

        # Construct JSON response manually
        response_data = {
            "message": "Hooray! Your parcel order has been created successfully!",
            "parcel": {
                "id": new_parcel.id,
                "pickup_location": new_parcel.pickup_location,
                "destination": new_parcel.destination,
                "weight": new_parcel.weight,
                "price": new_parcel.price,
                "description": new_parcel.description
            }
        }

        return make_response(jsonify(response_data), 201)



# Route 2: Get details of a parcel order by parcel ID
# @parcel_bp.route('/parcels/<int:parcel_id>', methods=['GET'])
class GetParcel(Resource):
    @jwt_required()
    def get(self, parcel_id):
        parcel = Parcel.query.filter_by(id=parcel_id).first()
        if parcel:
            return make_response(jsonify({"message": "Great! We found your parcel details!", "parcel": parcel.__repr__()}), 200)
        else:
            return make_response(jsonify({"message": "Oops! We couldn't find a parcel with that ID."}), 404)


# Route 3: Change destination of a specific parcel delivery order
# @parcel_bp.route('/parcels/<int:parcel_id>/destination', methods=['PUT'])
class ChangeRoute(Resource):
    @jwt_required()
    def put(self, parcel_id):
        user_id = get_jwt_identity()
        parcel = Parcel.query.get(parcel_id)
        if parcel and parcel.user_id == user_id and parcel.status != 'delivered':
            data = request.get_json()
            parcel.destination = data.get('destination')
            db.session.commit()
            return make_response(jsonify({"message": "Destination updated successfully! Your parcel is on its way to the new destination.", "parcel": parcel.__repr__()}), 200)
        else:
            return make_response(jsonify({"message": "Sorry, we can't change the destination of this parcel."}), 400)

# # Route 4: Cancel a specific parcel delivery order
# @parcel_bp.route('/parcels/<int:parcel_id>/cancel', methods=['PUT'])
class CancelParcel(Resource):
    @jwt_required
    def post(self, parcel_id):
        user_id = get_jwt_identity()
        parcel = Parcel.query.get(parcel_id)
        if parcel and parcel.user_id == user_id and parcel.status != 'delivered':
            parcel.status = 'cancelled'
            db.session.commit()
            return make_response(jsonify({"message": "Parcel cancelled successfully! We've halted delivery for this parcel.", "parcel": parcel.__repr__()}), 200)
        else:
            return make_response(jsonify({"message": "Sorry, we can't cancel this parcel."}), 400)


# # Route 5: Get a list of all parcel deliveries associated to a user
# @parcel_bp.route('/users/<int:user_id>/parcels', methods=['GET'])
class GetUserParcels(Resource):
    @jwt_required()
    def get(self, user_id):
        if user_id is None:
            return make_response(jsonify({"message": "User ID not found in token."}), 403)
        
        parcels = Parcel.query.filter_by(user_id=user_id).all()
        return make_response(jsonify({"message": "Here are all the parcels associated with this user!", "parcels": [parcel.__repr__() for parcel in parcels]}), 200)

api.add_resource(GetParcel, '/parcels/<int:parcel_id>')
api.add_resource(ViewAndCreateParcel, '/parcels')
api.add_resource(ChangeRoute, '/parcels/<int:parcel_id>/destination')
api.add_resource(CancelParcel, '/parcels/<int:parcel_id>/cancel')
api.add_resource(GetUserParcels, '/users/<int:user_id>/parcels')

