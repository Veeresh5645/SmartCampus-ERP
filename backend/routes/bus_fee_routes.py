from flask import Blueprint, request, jsonify

from database.db import db

from models.bus_fee_model import BusFee

bus_fee_bp = Blueprint(
    'bus_fee',
    __name__
)


# ADD BUS FEE
@bus_fee_bp.route(
    '/add',
    methods=['POST']
)
def add_bus_fee():

    try:

        data = request.get_json()

        bus_fee = BusFee(

            route_name=data.get(
                'route_name'
            ),

            bus_fee=float(
                data.get(
                    'bus_fee',
                    0
                ) or 0
            )
        )

        db.session.add(bus_fee)

        db.session.commit()

        return jsonify({

            "message":
                "Bus fee added"

        }), 201

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# GET BUS FEES
@bus_fee_bp.route(
    '/all',
    methods=['GET']
)
def get_bus_fees():

    try:

        bus_fees = BusFee.query.all()

        output = []

        for bus in bus_fees:

            output.append({

                "id":
                    bus.id,

                "route_name":
                    bus.route_name,

                "bus_fee":
                    bus.bus_fee
            })

        return jsonify(output)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500