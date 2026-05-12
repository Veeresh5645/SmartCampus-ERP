from flask import Blueprint, request, jsonify

from database.db import db

from models.fee_structure_model import FeeStructure
from models.bus_route_model import BusRoute

fee_bp = Blueprint('fee', __name__)

# ADD FEE STRUCTURE
@fee_bp.route('/add-fee-structure', methods=['POST'])
def add_fee_structure():

    data = request.get_json()

    fee_structure = FeeStructure(
        class_name=data.get('class_name'),
        admission_fee=data.get('admission_fee'),
        tuition_fee=data.get('tuition_fee'),
        is_bus_available=data.get('is_bus_available')
    )

    db.session.add(fee_structure)

    db.session.commit()

    return jsonify({
        "message": "Fee structure added successfully"
    }), 201


# ADD BUS ROUTE
@fee_bp.route('/add-bus-route', methods=['POST'])
def add_bus_route():

    data = request.get_json()

    bus_route = BusRoute(
        route_name=data.get('route_name'),
        location=data.get('location'),
        bus_fee=data.get('bus_fee')
    )

    db.session.add(bus_route)

    db.session.commit()

    return jsonify({
        "message": "Bus route added successfully"
    }), 201


# GET ALL FEE STRUCTURES
@fee_bp.route('/fee-structures', methods=['GET'])
def get_fee_structures():

    structures = FeeStructure.query.all()

    output = []

    for item in structures:

        output.append({
            "id": item.id,
            "class_name": item.class_name,
            "admission_fee": item.admission_fee,
            "tuition_fee": item.tuition_fee
        })

    return jsonify(output), 200


# GET ALL BUS ROUTES
@fee_bp.route('/bus-routes', methods=['GET'])
def get_bus_routes():

    routes = BusRoute.query.all()

    output = []

    for item in routes:

        output.append({
            "id": item.id,
            "route_name": item.route_name,
            "location": item.location,
            "bus_fee": item.bus_fee
        })

    return jsonify(output), 200