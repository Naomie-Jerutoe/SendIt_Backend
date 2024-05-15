from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import joinedload
from models import Parcel, User, db, Order
from flask_restful import Api, Resource
from auth_middleware import admin_required
from schemas import parcel
from flask_mail import Message
from extensions import mail


parcel_bp = Blueprint('parcel_bp', __name__)
ma = Marshmallow(parcel_bp)
api = Api(parcel_bp)

class ViewAndCreateParcel(Resource):
    @admin_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.is_admin:
            parcels = Parcel.query.all()
        return make_response(jsonify({"message": "As an admin, you have access to all parcels. Here they are!", 
                                "parcels": [
                                    {"id":parcel.id, 
                                    "pickup_location": parcel.pickup_location, 
                                    "destination": parcel.destination, 
                                    "weight":parcel.weight, 
                                    "price": parcel.price, 
                                    "description": parcel.description} for parcel in parcels]}), 200)
    
    @jwt_required
    def post(self):
        user_claims = get_jwt()
        user_id = user_claims['sub'].get('userId')

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
        
        result = parcel.dump(new_parcel)
        return make_response(jsonify({
            "message": "Hooray! Your parcel order has been created successfully!",
            "new_parcel": result
        }), 201)

api.add_resource(ViewAndCreateParcel, '/parcels')

# Route 2: Get details of a parcel order by parcel ID
class GetParcel(Resource):
    @jwt_required()
    @jwt_required()
    def get(self, parcel_id):
        parcel = Parcel.query.options(joinedload(Parcel.orders)).filter_by(id=parcel_id).first()

        if not parcel:
            return make_response(jsonify({"message": "Oops! We couldn't find a parcel with that ID."}), 404)

        order = parcel.orders[0] if parcel.orders else None
        status = order.status if order else None

        parcel_data = {
            "id": parcel.id,
            "pickup_location": parcel.pickup_location,
            "destination": parcel.destination,
            "weight": parcel.weight,
            "price": parcel.price,
            "description": parcel.description,
            "status": status,
            "user_id": parcel.user_id
        }

        return make_response(jsonify({
            "message": f"Parcel with ID {parcel_id} retrieved successfully",
            "parcel": parcel_data
        }), 200)

api.add_resource(GetParcel, '/parcels/<int:parcel_id>')

# Route 3: Change destination of a specific parcel delivery order
class ChangeRoute(Resource):
    @jwt_required()
    @jwt_required()
    def put(self, parcel_id):
        user_info = get_jwt_identity()
        user_id = user_info.get('userId')
        user_info = get_jwt_identity()
        user_id = user_info.get('userId')
        parcel = Parcel.query.get(parcel_id)

        if not parcel:
            return {"message": "Parcel not found."}, 404

        if parcel.user_id != user_id:
            return {"message": "Unauthorized access. You are not allowed to modify this parcel"}, 403

        order = Order.query.filter_by(parcel_id=parcel_id).first()

        if not order:
            return {"message": "Order not found."}, 404

        if order.status == 'delivered':
            return {"message": "Cannot change destination. The parcel has already been delivered."}, 400

        new_destination = request.json.get('destination')
        if not new_destination:
            return {"error": "Destination is required."}, 400

        parcel.destination = new_destination
        db.session.commit()

        response_data = {'message': 'Parcel destination updated successfully.'}
        return response_data, 200

api.add_resource(ChangeRoute, '/parcels/<int:parcel_id>/destination')

# # Route 4: Cancel a specific parcel delivery order
class CancelParcel(Resource):
    @jwt_required()
    @jwt_required()
    def post(self, parcel_id):
        user_info = get_jwt_identity()
        user_id = user_info.get('userId')
        user_info = get_jwt_identity()
        user_id = user_info.get('userId')
        parcel = Parcel.query.get(parcel_id)

        if not parcel:
            return {"message": "Parcel not found."}, 404

        if parcel.user_id != user_id:
            return {"message": "Unauthorized access. You are not allowed to cancel this parcel."}, 403

        order = Order.query.filter(Order.parcel_id==parcel_id).first()
        if not order:
            return {"message": "Order not found."}, 404

        if order.status == 'delivered':
            return {"message": "Cannot cancel. The parcel has already been delivered."}, 400

        order.status = 'canceled'
        db.session.commit()

        response_data = {
            "message": "Parcel cancelled successfully! We've halted delivery for this parcel."
        }

        return response_data, 200

api.add_resource(CancelParcel, '/parcels/<int:parcel_id>/cancel')

# # Route 5: Get a list of all parcel deliveries associated to a user
class GetUserParcels(Resource):
    @jwt_required()
    @jwt_required()
    def get(self, user_id):
        parcels = (
            Parcel.query.options(joinedload(Parcel.orders))
            .filter_by(user_id=user_id)
            .all()
        )

        if not parcels:
            return make_response(jsonify({"message": "No parcels found for this user"}), 404)

        parcel_data = []
        for parcel in parcels:
            order = parcel.orders[0] if parcel.orders else None
            status = order.status if order else None

            parcel_data.append({
                "id": parcel.id,
                "pickup_location": parcel.pickup_location,
                "destination": parcel.destination,
                "weight": parcel.weight,
                "price": parcel.price,
                "description": parcel.description,
                "status": status,
                "user_id": parcel.user_id
            })

        return make_response(jsonify({
            "message": f"Parcels associated with user ID {user_id} retrieved successfully",
            "parcels": parcel_data
        }), 200)
    
api.add_resource(GetUserParcels, '/users/<int:user_id>/parcels')