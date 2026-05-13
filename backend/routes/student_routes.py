from flask import Blueprint, request, jsonify

from database.db import db

from models.student_model import Student
from models.fee_structure_model import FeeStructure
from models.bus_route_model import BusRoute

student_bp = Blueprint(
    'students',
    __name__
)


# GET ALL STUDENTS
@student_bp.route(
    '/all',
    methods=['GET']
)
def get_students():

    try:

        students = Student.query.all()

        output = []

        for student in students:

            output.append({

                "id": student.id,

                "full_name": student.full_name,

                "admission_number":
                    student.admission_number,

                "joining_year":
                    student.joining_year,

                "academic_year":
                    student.academic_year,

                "current_class":
                    student.current_class,

                "paid_amount":
                    student.paid_amount,

                "remaining_amount":
                    student.remaining_amount,

                "total_fee":
                    student.total_fee
            })

        return jsonify(output)

    except Exception as e:

        print("GET STUDENT ERROR:")
        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# ADD STUDENT
@student_bp.route(
    '/add',
    methods=['POST']
)
def add_student():

    try:

        data = request.get_json()

        print("DATA RECEIVED:")
        print(data)

        fee_structure = FeeStructure.query.filter_by(

            academic_year=data.get(
                'academic_year'
            ),

            class_name=data.get(
                'current_class'
            )

        ).first()

        tuition_fee = 0
        admission_fee = 0
        bus_fee = 0

        if fee_structure:

            tuition_fee = (
                fee_structure.tuition_fee
            )

            if data.get(
                'admission_type'
            ) == 'new':

                admission_fee = (
                    fee_structure
                    .new_admission_fee
                )

            else:

                admission_fee = (
                    fee_structure
                    .old_admission_fee
                )

        if data.get('bus_required'):

            route = BusRoute.query.filter_by(

                route_name=data.get(
                    'bus_route'
                )

            ).first()

            if route:

                bus_fee = route.bus_fee

        old_due_total = 0

        for due in data.get(
            'old_dues',
            []
        ):

            old_due_total += int(

                due.get(
                    'pending_fee',
                    0
                ) or 0
            )

        total_fee = (

            int(tuition_fee or 0)

            +

            int(admission_fee or 0)

            +

            int(bus_fee or 0)

            +

            old_due_total
        )

        paid_amount = int(

            data.get(
                'paid_amount',
                0
            ) or 0
        )

        remaining_amount = (
            total_fee - paid_amount
        )

        student = Student(

            full_name=data.get(
                'full_name'
            ),

            admission_number=data.get(
                'admission_number'
            ),

            admission_type=data.get(
                'admission_type'
            ),

            joining_year=data.get(
                'joining_year'
            ),

            academic_year=data.get(
                'academic_year'
            ),

            current_class=data.get(
                'current_class'
            ),

            section=data.get(
                'section'
            ),

            parent_name=data.get(
                'parent_name'
            ),

            phone=data.get(
                'phone'
            ),

            address=data.get(
                'address'
            ),

            bus_required=data.get(
                'bus_required'
            ),

            bus_route=data.get(
                'bus_route'
            ),

            total_fee=total_fee,

            paid_amount=paid_amount,

            remaining_amount=remaining_amount
        )

        db.session.add(student)

        db.session.commit()

        return jsonify({

            "message":
                "Student added successfully"

        }), 201

    except Exception as e:

        print("STUDENT ADD ERROR:")
        print(e)

        return jsonify({
            "error": str(e)
        }), 500