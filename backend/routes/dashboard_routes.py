from flask import Blueprint, jsonify

from models.student_model import Student
from models.teacher_model import Teacher

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():

    total_students = Student.query.count()

    total_teachers = Teacher.query.count()

    students = Student.query.all()

    total_pending_fees = sum(
        student.remaining_amount for student in students
    )

    total_collected_fees = sum(
        student.paid_amount for student in students
    )

    return jsonify({

        "total_students": total_students,

        "total_teachers": total_teachers,

        "pending_fees": total_pending_fees,

        "collected_fees": total_collected_fees

    }), 200