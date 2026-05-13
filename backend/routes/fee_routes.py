from flask import Blueprint, request, jsonify

from database.db import db

from models.fee_structure_model import FeeStructure
from models.bus_route_model import BusRoute

fee_bp = Blueprint('fee', __name__)

# ADD FEE STRUCTURE
@fee_bp.route('/add-structure', methods=['POST'])
def add_fee_structure():

    try:

        data = request.get_json()

        fee = FeeStructure(

            academic_year=data.get(
                'academic_year'
            ),

            class_name=data.get(
                'class_name'
            ),

            tuition_fee=float(
                data.get('tuition_fee')
            ),

            new_admission_fee=float(
                data.get(
                    'new_admission_fee'
                )
            ),

            old_admission_fee=float(
                data.get(
                    'old_admission_fee'
                )
            )
        )

        db.session.add(fee)

        db.session.commit()

        return jsonify({
            "message":
                "Fee structure added"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# GET FEE STRUCTURES
@fee_bp.route('/structures', methods=['GET'])
def get_structures():

    fees = FeeStructure.query.all()

    output = []

    for fee in fees:

        output.append({

            "id": fee.id,

            "academic_year":
                fee.academic_year,

            "class_name":
                fee.class_name,

            "tuition_fee":
                fee.tuition_fee,

            "new_admission_fee":
                fee.new_admission_fee,

            "old_admission_fee":
                fee.old_admission_fee
        })

    return jsonify(output), 200


# DELETE FEE STRUCTURE
@fee_bp.route(
    '/delete-structure/<int:id>',
    methods=['DELETE']
)
def delete_structure(id):

    fee = FeeStructure.query.get(id)

    if not fee:

        return jsonify({
            "message":
                "Structure not found"
        }), 404

    db.session.delete(fee)

    db.session.commit()

    return jsonify({
        "message":
            "Fee structure deleted"
    }), 200


# ADD BUS ROUTE
@fee_bp.route('/add-route', methods=['POST'])
def add_route():

    data = request.get_json()

    route = BusRoute(

        route_name=data.get(
            'route_name'
        ),

        bus_fee=float(
            data.get('bus_fee')
        )
    )

    db.session.add(route)

    db.session.commit()

    return jsonify({
        "message":
            "Bus route added"
    }), 201


# GET ROUTES
@fee_bp.route('/routes', methods=['GET'])
def get_routes():

    routes = BusRoute.query.all()

    output = []

    for route in routes:

        output.append({

            "id": route.id,

            "route_name":
                route.route_name,

            "bus_fee":
                route.bus_fee
        })

    return jsonify(output), 200