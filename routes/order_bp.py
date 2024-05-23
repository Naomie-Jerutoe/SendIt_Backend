from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from models import Order, db, User, Parcel
from schemas import OrderSchema
from auth_middleware import admin_required
from flask_mail import Message
from extensions import mail

# Create a Blueprint for order-related routes with prefix '/api/orders'
orders_bp = Blueprint('orders_bp', __name__,)
ma = Marshmallow(orders_bp)
api = Api(orders_bp)

class OrderResource(Resource):
    @admin_required
    def get(self):
        orders = Order.query.all()
        order_statuses = [{'id': order.id, 'status': order.status, 'parcel_id': order.parcel_id} for order in orders]
        return make_response(jsonify({'order_statuses': order_statuses}),200)

    @admin_required
    def post(self):    
        data = request.get_json()
        
        parcel_id = data.get('parcel_id')
        status = data.get('status')
        
        order = Order(parcel_id=parcel_id, status=status)
        
        db.session.add(order)
        db.session.commit()
        return make_response(jsonify({"msg": "Order status created successfully"}), 201)

api.add_resource(OrderResource, '/orders')

class OrderDetailResource(Resource):
    @jwt_required()
    def get(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        
        if order is None:
            return make_response(jsonify({'message': 'Order not found'}), 404)
        
        order_status = {
            'id': order.id,
            'status': order.status,
            'parcel_id': order.parcel_id
        }
        
        return make_response(jsonify({'order_status': order_status}), 200)
    
    @admin_required
    def put(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"msg": "Order not found"}), 404
        
        data = request.get_json()
        new_status = data.get('status')
        if new_status not in ['delivered', 'enroute', 'canceled']:
            return {'error': 'Invalid status'}, 400
        order.status = new_status
        
        db.session.commit()
        
        user_email = order.parcels.users.email
        user_username = order.parcels.users.username
        send_email_notification(user_email, new_status, user_username)
        
        return make_response(jsonify({"msg": "Order status updated successfully"}), 200)
    
    @admin_required
    def delete(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        
        if order is None:
            return make_response(jsonify({'message': 'Order not found'}), 404)
        
        db.session.delete(order)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Order deleted successfully'}), 200)

api.add_resource(OrderDetailResource, '/orders/<int:order_id>')

def send_email_notification(recipient_email, status, username):
    msg = Message('Order Status Update', sender='senditapp.cci@gmail.com', recipients=[recipient_email])
    msg.body = f'Dear {username}, \n\n Your parcel has been {status}. \n\nThank You. \n\nSendIt Parcel Delivery Services'
    mail.send(msg)

















# @orders_bp.route('/', methods=['POST'])
# @jwt_required()
# def create_order():
#     try:
#         data = request.get_json()
#         current_user_id = get_jwt_identity()
#         order_data = {
#             'parcel': data['parcel'],
#             'status': 'enroute'
#         }
#         new_order = orderSchema.load(order_data, session=db.session)
#         db.session.commit()

#         return jsonify({'message': 'Order created successfully'}), 201
#     except ValidationError as err:
#         return jsonify({'error': err.messages}), 400

# @orders_bp.route('/<int:order_id>', methods=['PUT'])
# @jwt_required()
# @admin_required  # Decorate the function with the admin_required decorator
# def update_order(order_id):
#     try:
#         data = request.get_json()
#         order = Order.query.get(order_id)
#         if not order:
#             return jsonify({'error': 'Order not found'}), 404

#         # Update the order status if provided in the request data
#         if 'status' in data:
#             order.status = data['status']

#         db.session.commit()

#         return jsonify({'message': 'Order updated successfully'}), 200
#     except ValidationError as err:
#         return jsonify({'error': err.messages}), 400