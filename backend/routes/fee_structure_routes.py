from flask import Blueprint, request, jsonify

from database.db import db

from models.fee_structure_model import FeeStructure

fee_structure_bp = Blueprint(
    'fee_structure',
    __name__
)


# ADD FEE STRUCTURE
@fee_structure_bp.route(
    '/add',
    methods=['POST']
)
def add_fee_structure():

    try:

        data = request.get_json()

        fee_structure = FeeStructure(

            academic_year=data.get(
                'academic_year'
            ),

            class_name=data.get(
                'class_name'
            ),

            tuition_fee=float(
                data.get(
                    'tuition_fee',
                    0
                ) or 0
            ),

            bus_route=data.get(
                'bus_route'
            ),

            bus_fee=float(
                data.get(
                    'bus_fee',
                    0
                ) or 0
            ),

            new_admission_fee=float(
                data.get(
                    'new_admission_fee',
                    0
                ) or 0
            ),

            old_admission_fee=float(
                data.get(
                    'old_admission_fee',
                    0
                ) or 0
            )
        )

        db.session.add(
            fee_structure
        )

        db.session.commit()

        return jsonify({

            "message":
                "Fee structure added"

        }), 201

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# GET ALL FEE STRUCTURES
@fee_structure_bp.route(
    '/all',
    methods=['GET']
)
def get_fee_structures():

    try:

        fee_structures = FeeStructure.query.all()

        output = []

        for fee in fee_structures:

            output.append({

                "id":
                    fee.id,

                "academic_year":
                    fee.academic_year,

                "class_name":
                    fee.class_name,

                "tuition_fee":
                    fee.tuition_fee,

                "bus_route":
                    fee.bus_route,

                "bus_fee":
                    fee.bus_fee,

                "new_admission_fee":
                    fee.new_admission_fee,

                "old_admission_fee":
                    fee.old_admission_fee
            })

        return jsonify(output)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500