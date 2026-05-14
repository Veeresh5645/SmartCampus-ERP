from flask import Blueprint, request, jsonify

from database.db import db

from models.student_model import Student

student_bp = Blueprint(
    'students',
    __name__
)


# ADD STUDENT
@student_bp.route(
    '/add',
    methods=['POST']
)
def add_student():

    try:

        data = request.get_json()

        student = Student(

            full_name=data.get(
                'full_name'
            ),

            admission_number=data.get(
                'admission_number'
            ),

            current_class=data.get(
                'current_class'
            ),

            academic_year=data.get(
                'academic_year'
            ),

            bus_required=data.get(
                'bus_required'
            ),

            bus_route=data.get(
                'bus_route'
            ),

            total_fees=float(
                data.get(
                    'total_fees',
                    0
                ) or 0
            ),

            paid_amount=float(
                data.get(
                    'paid_amount',
                    0
                ) or 0
            ),

            remaining_amount=float(
                data.get(
                    'remaining_amount',
                    0
                ) or 0
            )
        )

        db.session.add(student)

        db.session.commit()

        return jsonify({

            "message":
                "Student saved successfully"

        }), 201

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


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

                "id":
                    student.id,

                "full_name":
                    student.full_name,

                "admission_number":
                    student.admission_number,

                "current_class":
                    student.current_class,

                "academic_year":
                    student.academic_year,

                "bus_required":
                    student.bus_required,

                "bus_route":
                    student.bus_route,

                "total_fees":
                    student.total_fees,

                "paid_amount":
                    student.paid_amount,

                "remaining_amount":
                    student.remaining_amount
            })

        return jsonify(output)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500