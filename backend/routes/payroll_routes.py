from flask import Blueprint, request, jsonify

from database.db import db

from models.teacher_model import Teacher
from models.teacher_attendance_model import TeacherAttendance
from models.salary_record_model import SalaryRecord
from models.expense_model import Expense

from datetime import datetime

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
                "Attendance saved"

        }), 201

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# GENERATE MONTHLY PAYROLL
@payroll_bp.route(
    '/generate-payroll',
    methods=['POST']
)
def generate_payroll():

    try:

        data = request.get_json()

        month = data.get('month')

        teachers = Teacher.query.all()

        for teacher in teachers:

            existing_record = SalaryRecord.query.filter_by(

                teacher_id=teacher.id,

                month=month

            ).first()

            if existing_record:

                continue

            attendance_records = TeacherAttendance.query.filter(

                TeacherAttendance.teacher_id == teacher.id,

                TeacherAttendance.attendance_date.like(
                    f'{month}%'
                ),

                TeacherAttendance.status == 'Present'

            ).all()

            attended_days = len(
                attendance_records
            )

            working_days = 26

            monthly_salary = int(
                teacher.salary or 0
            )

            per_day_salary = (
                monthly_salary / working_days
            )

            final_salary = (
                per_day_salary * attended_days
            )

            salary_record = SalaryRecord(

                teacher_id=teacher.id,

                month=month,

                working_days=working_days,

                attended_days=attended_days,

                calculated_salary=final_salary,

                is_paid=False
            )

            db.session.add(
                salary_record
            )

        db.session.commit()

        return jsonify({

            "message":
                "Payroll generated"

        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# GET MONTHLY SALARY RECORDS
@payroll_bp.route(
    '/salary-records/<month>',
    methods=['GET']
)
def get_salary_records(month):

    try:

        records = SalaryRecord.query.filter_by(
            month=month
        ).all()

        output = []

        for record in records:

            teacher = Teacher.query.get(
                record.teacher_id
            )

            output.append({

                "id":
                    record.id,

                "teacher_name":
                    teacher.full_name
                    if teacher else "",

                "working_days":
                    record.working_days,

                "attended_days":
                    record.attended_days,

                "salary":
                    record.calculated_salary,

                "is_paid":
                    record.is_paid,

                "payment_mode":
                    record.payment_mode,

                "paid_date":
                    record.paid_date
            })

        return jsonify(output)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# PAY SALARY
@payroll_bp.route(
    '/pay-salary/<int:salary_id>',
    methods=['POST']
)
def pay_salary(salary_id):

    try:

        data = request.get_json()

        salary_record = SalaryRecord.query.get(
            salary_id
        )

        if not salary_record:

            return jsonify({

                "message":
                    "Salary record not found"

            }), 404

        # PREVENT DOUBLE PAYMENT
        if salary_record.is_paid:

            return jsonify({

                "message":
                    "Salary already paid"

            })

        salary_record.is_paid = True

        salary_record.payment_mode = data.get(
            'payment_mode'
        )

        salary_record.paid_date = str(
            datetime.now().date()
        )

        db.session.commit()

        # GET TOTAL PAID SALARY OF MONTH
        paid_records = SalaryRecord.query.filter_by(

            month=salary_record.month,

            is_paid=True

        ).all()

        total_salary_paid = sum([

            item.calculated_salary

            for item in paid_records
        ])

        # MONTH NAME FORMAT
        month_text = salary_record.month

        year = month_text[:4]

        month_number = month_text[5:7]

        month_names = {

            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }

        month_name = month_names.get(
            month_number,
            month_number
        )

        comment_text = (
            f'Salary paid for {month_name} {year}'
        )

        existing_expense = Expense.query.filter_by(

            category='Salary',

            comment=comment_text

        ).first()

        # CREATE OR UPDATE EXPENSE
        if not existing_expense:

            expense = Expense(

                category='Salary',

                amount=total_salary_paid,

                comment=comment_text,

                expense_date=str(
                    datetime.now().date()
                )
            )

            db.session.add(expense)

        else:

            existing_expense.amount = (
                total_salary_paid
            )

        db.session.commit()

        return jsonify({

            "message":
                "Salary paid successfully"

        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500