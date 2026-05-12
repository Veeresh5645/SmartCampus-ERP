from flask import Blueprint, request, jsonify

from database.db import db

from models.student_model import Student

student_bp = Blueprint('student', __name__)

# ADD STUDENT
@student_bp.route('/add', methods=['POST'])
def add_student():

    try:

        data = request.get_json()

        admission_fee = float(data.get('admission_fee', 0))

        tuition_fee = float(data.get('tuition_fee', 0))

        bus_fee = float(data.get('bus_fee', 0))

        previous_due = float(data.get('previous_due', 0))

        paid_amount = float(data.get('paid_amount', 0))

        total_fee = (
            admission_fee +
            tuition_fee +
            bus_fee +
            previous_due
        )

        remaining_amount = total_fee - paid_amount

        student = Student(

            full_name=data.get('full_name'),

            admission_number=data.get('admission_number'),

            admission_type=data.get('admission_type'),

            joining_year=data.get('joining_year'),

            current_class=data.get('current_class'),

            section=data.get('section'),

            parent_name=data.get('parent_name'),

            phone=data.get('phone'),

            address=data.get('address'),

            bus_required=data.get('bus_required'),

            bus_route=data.get('bus_route'),

            admission_fee=admission_fee,

            tuition_fee=tuition_fee,

            bus_fee=bus_fee,

            previous_due=previous_due,

            total_fee=total_fee,

            paid_amount=paid_amount,

            remaining_amount=remaining_amount
        )

        db.session.add(student)

        db.session.commit()

        return jsonify({
            "message": "Student added successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# GET ALL STUDENTS
@student_bp.route('/all', methods=['GET'])
def get_students():

    students = Student.query.all()

    output = []

    for student in students:

        output.append({

            "id": student.id,

            "full_name": student.full_name,

            "admission_number": student.admission_number,

            "admission_type": student.admission_type,

            "joining_year": student.joining_year,

            "current_class": student.current_class,

            "section": student.section,

            "previous_due": student.previous_due,

            "remaining_amount": student.remaining_amount
        })

    return jsonify(output), 200