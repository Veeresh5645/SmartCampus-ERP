from flask import Blueprint, request, jsonify

from database.db import db

from models.student_model import Student
from models.fee_structure_model import FeeStructure
from models.bus_route_model import BusRoute
from models.old_due_model import OldDue

student_bp = Blueprint('student', __name__)

# ADD STUDENT
@student_bp.route('/add', methods=['POST'])
def add_student():

    try:

        data = request.get_json()

        academic_year = data.get('academic_year')

        current_class = data.get('current_class')

        # FETCH FEE STRUCTURE
        fee_structure = FeeStructure.query.filter_by(
            academic_year=academic_year,
            class_name=current_class
        ).first()

        if not fee_structure:

            return jsonify({
                "message": "Fee structure not found"
            }), 404

        tuition_fee = fee_structure.tuition_fee

        if data.get('admission_type') == 'new':
            admission_fee = (
                fee_structure.new_admission_fee
            )

        else:
            admission_fee = (
                fee_structure.old_admission_fee
            )

        # BUS LOGIC
        bus_required = data.get('bus_required')

        bus_fee = 0

        if bus_required:

            route = BusRoute.query.filter_by(
                route_name=data.get('bus_route')
            ).first()

            if route:

                bus_fee = route.bus_fee

        # OLD DUES
        total_old_due = 0

        old_dues = data.get('old_dues', [])

        for due in old_dues:

            pending = float(due.get('pending_fee', 0))

            total_old_due += pending

        total_fee = (
            tuition_fee +
            admission_fee +
            bus_fee +
            total_old_due
        )

        paid_amount = float(
            data.get('paid_amount', 0)
        )

        remaining_amount = total_fee - paid_amount

        # CREATE STUDENT
        student = Student(

            full_name=data.get('full_name'),

            admission_number=data.get('admission_number'),

            admission_type=data.get('admission_type'),

            joining_year=data.get('joining_year'),

            current_class=current_class,

            section=data.get('section'),

            parent_name=data.get('parent_name'),

            phone=data.get('phone'),

            address=data.get('address'),

            bus_required=bus_required,

            bus_route=data.get('bus_route'),

            admission_fee=admission_fee,

            tuition_fee=tuition_fee,

            bus_fee=bus_fee,

            previous_due=total_old_due,

            total_fee=total_fee,

            paid_amount=paid_amount,

            remaining_amount=remaining_amount
        )

        db.session.add(student)

        db.session.commit()

        # SAVE YEAR-WISE DUES
        for due in old_dues:

            old_due = OldDue(

                student_admission_number=data.get(
                    'admission_number'
                ),

                academic_year=due.get('academic_year'),

                pending_fee=due.get('pending_fee')
            )

            db.session.add(old_due)

        db.session.commit()

        return jsonify({
            "message": "Student added successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# GET STUDENTS
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

            "current_class": student.current_class,

            "total_fee": student.total_fee,

            "paid_amount": student.paid_amount,

            "remaining_amount": student.remaining_amount
        })

    return jsonify(output), 200