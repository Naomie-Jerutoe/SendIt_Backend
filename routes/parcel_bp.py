from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Parcel, User, db, Order
from flask_restful import Api, Resource
from auth_middleware import admin_required
#from flask_mail import Message
#from extensions import mail

parcel_bp = Blueprint('parcel_bp', __name__)
api = Api(parcel_bp)

class ViewAndCreateParcel(Resource):
    @jwt_required()
    def get(self):
        try:
            user_info = get_jwt_identity()
            user_id = user_info.get('userId')
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
        except Exception as e:
            return make_response(jsonify({"message": "Internal Server Error", "error": str(e)}), 500)
   
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
        
        #create a new order for the parcel
        new_order = Order(parcel_id=new_parcel.id, status = 'enroute')
        db.session.add(new_order)
        db.session.commit()

        response_data = {
            "message": "Hooray! Your parcel order has been created successfully!",
            "parcel": {
                "id": new_parcel.id,
                "pickup_location": new_parcel.pickup_location,
                "destination": new_parcel.destination,
                "weight": new_parcel.weight,
                "price": new_parcel.price,
                "description": new_parcel.description
            },
            "order":{
                "id": new_order.id,
                "status": new_order.status
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

class CancelParcel(Resource):
    @jwt_required()
    def post(self, parcel_id):
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


# # Route 5: Get a list of all parcel deliveries associated to a user
# @parcel_bp.route('/users/<int:user_id>/parcels', methods=['GET'])
class GetUserParcels(Resource):
    @jwt_required()
    def get(self, user_id):
        if user_id is None:
            return make_response(jsonify({"message": "User ID not found in token."}), 403)
        
        parcels = Parcel.query.filter_by(user_id=user_id).all()
        return make_response(jsonify({"message": "Here are all the parcels associated with this user!", "parcels": [parcel.__repr__() for parcel in parcels]}), 200)
    

#Orders routes

# def send_order_status_email(recipient_email, order_status, parcel_id):
#     print(f"mail instance: {mail}")
#     msg = Message(
#         subject=f"Order Status Update for Parcel #{parcel_id}",
#         recipients=[recipient_email],
#         sender="mailtrap@demomailtrap.com"
#         )
#     msg.body = f"The status of your parcel #{parcel_id} has been updated to: {order_status}"
#     mail.send(msg)

# class UpdateOrderStatus(Resource):
#     @jwt_required()
#     def put(self, order_id):
#         user_info = get_jwt_identity()
#         user_id = user_info.get('userId')
        
#         if user_id is None:
#             return make_response(jsonify({"message": "User ID not found in token."}), 403)

#         user = User.query.get(user_id)
#         if user is None:
#             return make_response(jsonify({"message": "User not found."}), 404)

#         if not user.is_admin:
#             return make_response(jsonify({"message": "Unauthorized access. Only admins can update order status."}), 403)

#         order = Order.query.get(order_id)
#         if not order:
#             return make_response(jsonify({"message": "Order not found."}), 404)

#         new_status = request.json.get('status')
#         if not new_status:
#             return make_response(jsonify({"message": "Status is required."}), 400)

#         if new_status not in ['delivered', 'enroute', 'canceled']:
#             return make_response(jsonify({"message": "Invalid status."}), 400)

#         order.status = new_status
#         db.session.commit()
        
#         # parcel = Parcel.query.get(order.parcel_id)
#         # #send email notification
#         # send_order_status_email(user.email, order.status, parcel.id)
        
#         response_data = {
#             "message": "Order status updated successfully.",
#             "order": {
#                 "id": order.id,
#                 "status": order.status,
#                 "parcel_id": order.parcel_id
#             }
#         }

#         return make_response(jsonify(response_data), 200)
    
# class GetAllOrders(Resource):
#     @jwt_required()
#     def get(self):
#         user_info = get_jwt_identity()
#         user_id = user_info.get('userId')

#         if user_id is None:
#             return make_response(jsonify({"message": "User ID not found in token."}), 403)

#         user = User.query.get(user_id)
#         if user is None:
#             return make_response(jsonify({"message": "User not found."}), 404)

#         if not user.is_admin:
#             return make_response(jsonify({"message": "Unauthorized access. Only admins can view all orders."}), 403)

#         orders = Order.query.all()
#         order_list = [
#             {
#                 "id": order.id,
#                 "status": order.status,
#                 "parcel_id": order.parcel_id
#             }
#             for order in orders
#         ]
#         return make_response(jsonify({"orders": order_list}), 200)

api.add_resource(GetParcel, '/parcels/<int:parcel_id>')
api.add_resource(ViewAndCreateParcel, '/parcels')
api.add_resource(ChangeRoute, '/parcels/<int:parcel_id>/destination')
api.add_resource(CancelParcel, '/parcels/<int:parcel_id>/cancel')
api.add_resource(GetUserParcels, '/users/<int:user_id>/parcels')
#api.add_resource(UpdateOrderStatus, '/orders/<int:order_id>/status')
#api.add_resource(GetAllOrders, '/orders')