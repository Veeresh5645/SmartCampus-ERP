from flask import Blueprint, request, jsonify

from database.db import db

from models.attendance_model import Attendance

attendance_bp = Blueprint('attendance', __name__)

# MARK ATTENDANCE
@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():

    data = request.get_json()

    attendance = Attendance(
        student_name=data.get('student_name'),
        class_name=data.get('class_name'),
        date=data.get('date'),
        status=data.get('status')
    )

    db.session.add(attendance)

    db.session.commit()

    return jsonify({
        "message": "Attendance marked successfully"
    }), 201


# GET ATTENDANCE
@attendance_bp.route('/all', methods=['GET'])
def get_attendance():

    attendance = Attendance.query.all()

    output = []

    for item in attendance:

        output.append({
            "id": item.id,
            "student_name": item.student_name,
            "class_name": item.class_name,
            "date": item.date,
            "status": item.status
        })

    return jsonify(output), 200