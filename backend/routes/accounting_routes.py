from flask import Blueprint, request, jsonify

from database.db import db

from models.student_model import Student
from models.fee_payment_model import FeePayment
from models.expense_model import Expense

from datetime import datetime

accounting_bp = Blueprint(
    'accounting',
    __name__
)

# COLLECT FEES
@accounting_bp.route(
    '/collect-fees',
    methods=['POST']
)
def collect_fees():

    try:

        data = request.get_json()

        student = Student.query.filter_by(
            admission_number=data.get(
                'admission_number'
            )
        ).first()

        if not student:

            return jsonify({
                "message": "Student not found"
            }), 404

        amount = float(
            data.get('amount_paid')
        )

        student.paid_amount += amount

        student.remaining_amount -= amount

        receipt_number = (
            f"RCPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        payment = FeePayment(

            receipt_number=receipt_number,

            student_name=student.full_name,

            admission_number=student.admission_number,

            academic_year=data.get(
                'academic_year'
            ),

            class_name=student.current_class,

            amount_paid=amount,

            payment_mode=data.get(
                'payment_mode'
            ),

            transaction_id=data.get(
                'transaction_id'
            ),

            collected_by=data.get(
                'collected_by'
            ),

            payment_date=str(
                datetime.now()
            )
        )

        db.session.add(payment)

        db.session.commit()

        return jsonify({

            "message": "Fees collected",

            "receipt_number": receipt_number

        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# GET PAYMENTS
@accounting_bp.route(
    '/payments',
    methods=['GET']
)
def get_payments():

    payments = FeePayment.query.all()

    output = []

    for payment in payments:

        output.append({

            "receipt_number":
                payment.receipt_number,

            "student_name":
                payment.student_name,

            "amount_paid":
                payment.amount_paid,

            "payment_mode":
                payment.payment_mode,

            "payment_date":
                payment.payment_date
        })

    return jsonify(output), 200


# ADD EXPENSE
@accounting_bp.route(
    '/add-expense',
    methods=['POST']
)
def add_expense():

    try:

        data = request.get_json()

        if not data.get('comment'):

            return jsonify({
                "message": "Comment required"
            }), 400

        expense = Expense(

            expense_date=data.get(
                'expense_date'
            ),

            category=data.get(
                'category'
            ),

            amount=data.get(
                'amount'
            ),

            payment_mode=data.get(
                'payment_mode'
            ),

            comment=data.get(
                'comment'
            ),

            added_by=data.get(
                'added_by'
            ),

            academic_year=data.get(
                'academic_year'
            )
        )

        db.session.add(expense)

        db.session.commit()

        return jsonify({
            "message": "Expense added"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# GET EXPENSES
@accounting_bp.route(
    '/expenses',
    methods=['GET']
)
def get_expenses():

    category = request.args.get(
        'category'
    )

    academic_year = request.args.get(
        'academic_year'
    )

    expenses = Expense.query

    if category:

        expenses = expenses.filter_by(
            category=category
        )

    if academic_year:

        expenses = expenses.filter_by(
            academic_year=academic_year
        )

    expenses = expenses.all()

    output = []

    for expense in expenses:

        output.append({

            "expense_date":
                expense.expense_date,

            "category":
                expense.category,

            "amount":
                expense.amount,

            "payment_mode":
                expense.payment_mode,

            "comment":
                expense.comment,

            "academic_year":
                expense.academic_year
        })

    return jsonify(output), 200