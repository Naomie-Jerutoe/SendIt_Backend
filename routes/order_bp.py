from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from models import Order, db, User
from schemas import OrderSchema, orderSchema
from auth_middleware import admin_required  #Import the admin_required decorator

# Create a Blueprint for order-related routes with the prefix '/api/v1/orders'
orders_bp = Blueprint('orders', __name__, url_prefix='/api/v1/orders')

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        order_data = {
            'parcel': data['parcel'],
            'status': 'enroute'
        }
        new_order = orderSchema.load(order_data, session=db.session)
        db.session.commit()

        return jsonify({'message': 'Order created successfully'}), 201
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

@orders_bp.route('/<int:order_id>', methods=['PUT'])
@jwt_required()
@admin_required  # Decorate the function with the admin_required decorator
def update_order(order_id):
    try:
        data = request.get_json()
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Update the order status if provided in the request data
        if 'status' in data:
            order.status = data['status']

        db.session.commit()

        return jsonify({'message': 'Order updated successfully'}), 200
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400