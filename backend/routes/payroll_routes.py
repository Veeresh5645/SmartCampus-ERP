from flask import Blueprint, request, jsonify

from database.db import db

from models.teacher_model import Teacher
from models.teacher_attendance_model import TeacherAttendance
from models.salary_record_model import SalaryRecord

payroll_bp = Blueprint('payroll', __name__)

# MARK TEACHER ATTENDANCE
@payroll_bp.route('/mark-attendance', methods=['POST'])
def mark_teacher_attendance():

    data = request.get_json()

    attendance = TeacherAttendance(

        teacher_id=data.get('teacher_id'),

        teacher_name=data.get('teacher_name'),

        attendance_date=data.get('attendance_date'),

        status=data.get('status')
    )

    db.session.add(attendance)

    db.session.commit()

    return jsonify({
        "message": "Teacher attendance marked"
    }), 201


# GENERATE SALARY
@payroll_bp.route('/generate-salary', methods=['POST'])
def generate_salary():

    data = request.get_json()

    teacher_id = data.get('teacher_id')

    month = data.get('month')

    working_days = int(
        data.get('working_days')
    )

    teacher = Teacher.query.get(teacher_id)

    if not teacher:

        return jsonify({
            "message": "Teacher not found"
        }), 404

    attendance_records = TeacherAttendance.query.filter_by(
        teacher_id=teacher_id,
        status="Present"
    ).all()

    attended_days = len(attendance_records)

    per_day_salary = (
        teacher.salary / working_days
    )

    calculated_salary = (
        per_day_salary * attended_days
    )

    salary_record = SalaryRecord(

        teacher_id=teacher.id,

        teacher_name=teacher.full_name,

        month=month,

        total_working_days=working_days,

        attended_days=attended_days,

        monthly_salary=teacher.salary,

        calculated_salary=calculated_salary
    )

    db.session.add(salary_record)

    db.session.commit()

    return jsonify({

        "teacher": teacher.full_name,

        "working_days": working_days,

        "attended_days": attended_days,

        "calculated_salary": calculated_salary

    }), 200


# GET SALARY RECORDS
@payroll_bp.route('/salary-records', methods=['GET'])
def salary_records():

    records = SalaryRecord.query.all()

    output = []

    for record in records:

        output.append({

            "id": record.id,

            "teacher_name": record.teacher_name,

            "month": record.month,

            "working_days": record.total_working_days,

            "attended_days": record.attended_days,

            "salary": record.calculated_salary
        })

    return jsonify(output), 200