from flask import Blueprint, request, jsonify, send_file

from database.db import db
from models.student_model import Student

from reportlab.pdfgen import canvas

import os

student_bp = Blueprint('student', __name__)

# ADD STUDENT
@student_bp.route('/add', methods=['POST'])
def add_student():

    data = request.get_json()

    admission_fee = float(data.get('admission_fee', 0))
    tuition_fee = float(data.get('tuition_fee', 0))
    bus_fee = float(data.get('bus_fee', 0))
    old_due = float(data.get('old_due', 0))

    total_fee = admission_fee + tuition_fee + bus_fee + old_due

    paid_amount = float(data.get('paid_amount', 0))

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
        old_due=old_due,
        total_fee=total_fee,
        paid_amount=paid_amount,
        remaining_amount=remaining_amount
    )

    db.session.add(student)

    db.session.commit()

    return jsonify({
        "message": "Student added successfully"
    }), 201


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
            "class": student.current_class,
            "section": student.section,
            "paid_amount": student.paid_amount,
            "remaining_amount": student.remaining_amount
        })

    return jsonify(output), 200


# UPDATE STUDENT
@student_bp.route('/update/<int:id>', methods=['PUT'])
def update_student(id):

    student = Student.query.get(id)

    if not student:

        return jsonify({
            "message": "Student not found"
        }), 404

    data = request.get_json()

    student.full_name = data.get(
        'full_name',
        student.full_name
    )

    student.current_class = data.get(
        'current_class',
        student.current_class
    )

    student.section = data.get(
        'section',
        student.section
    )

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully"
    }), 200


# PAY FEES
@student_bp.route('/pay-fees/<int:id>', methods=['PUT'])
def pay_fees(id):

    student = Student.query.get(id)

    if not student:

        return jsonify({
            "message": "Student not found"
        }), 404

    data = request.get_json()

    amount = float(data.get('amount', 0))

    student.paid_amount += amount

    student.remaining_amount -= amount

    db.session.commit()

    return jsonify({
        "message": "Fees updated successfully"
    }), 200


# GENERATE RECEIPT PDF
@student_bp.route('/receipt/<int:id>', methods=['GET'])
def generate_receipt(id):

    student = Student.query.get(id)

    if not student:

        return jsonify({
            "message": "Student not found"
        }), 404

    filename = f"receipt_{student.id}.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(180, 800, "SmartCampus ERP")

    c.setFont("Helvetica", 14)

    c.drawString(50, 740, f"Student Name: {student.full_name}")

    c.drawString(50, 710, f"Admission No: {student.admission_number}")

    c.drawString(50, 680, f"Class: {student.current_class}")

    c.drawString(50, 650, f"Paid Amount: ₹ {student.paid_amount}")

    c.drawString(50, 620, f"Remaining Fees: ₹ {student.remaining_amount}")

    c.drawString(50, 560, "Fee Receipt Generated Successfully")

    c.save()

    return send_file(
        filename,
        as_attachment=True
    )


# DELETE STUDENT
@student_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):

    student = Student.query.get(id)

    if not student:

        return jsonify({
            "message": "Student not found"
        }), 404

    db.session.delete(student)

    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200