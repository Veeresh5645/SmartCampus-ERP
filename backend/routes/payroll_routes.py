from flask import Blueprint, request, jsonify

from database.db import db

from models.teacher_model import Teacher
from models.teacher_attendance_model import TeacherAttendance
from models.salary_record_model import SalaryRecord
from models.working_day_model import WorkingDay

payroll_bp = Blueprint(
    'payroll',
    __name__
)


# SAVE ATTENDANCE
@payroll_bp.route(
    '/bulk-attendance',
    methods=['POST']
)
def bulk_attendance():

    try:

        data = request.get_json()

        working_day = WorkingDay(

            attendance_date=data.get(
                'attendance_date'
            ),

            is_working_day=data.get(
                'is_working_day'
            ),

            holiday_reason=data.get(
                'holiday_reason'
            )
        )

        db.session.add(working_day)

        records = data.get(
            'attendance_records',
            []
        )

        for record in records:

            attendance = TeacherAttendance(

                teacher_id=record.get(
                    'teacher_id'
                ),

                attendance_date=data.get(
                    'attendance_date'
                ),

                status=record.get(
                    'status'
                )
            )

            db.session.add(attendance)

        db.session.commit()

        return jsonify({

            "message":
                "Attendance saved successfully"

        }), 201

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# GET SALARY RECORDS
@payroll_bp.route(
    '/salary-records',
    methods=['GET']
)
def get_salary_records():

    try:

        records = SalaryRecord.query.all()

        output = []

        for record in records:

            teacher = Teacher.query.get(
                record.teacher_id
            )

            output.append({

                "teacher_name":
                    teacher.full_name
                    if teacher else "",

                "month":
                    record.month,

                "working_days":
                    record.working_days,

                "attended_days":
                    record.attended_days,

                "salary":
                    record.salary
            })

        return jsonify(output)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500