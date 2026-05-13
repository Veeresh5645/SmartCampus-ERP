from flask import Blueprint, request, jsonify

from database.db import db

from models.student_model import Student
from models.fee_payment_model import FeePayment

from datetime import datetime

fee_bp = Blueprint(
    'fees',
    __name__
)


# COLLECT FEES
@fee_bp.route(
    '/collect',
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

                "message":
                    "Student not found"

            }), 404

        paid_amount = float(

            data.get(
                'paid_amount',
                0
            ) or 0
        )

        student.paid_amount += paid_amount

        student.remaining_amount -= paid_amount

        receipt_number = (

            "RCPT-"

            +

            str(int(
                datetime.now().timestamp()
            ))
        )

        payment = FeePayment(

            student_id=student.id,

            amount=paid_amount,

            payment_date=str(
                datetime.now().date()
            ),

            receipt_number=receipt_number,

            payment_mode=data.get(
                'payment_mode'
            ),

            academic_year=student.academic_year,

            class_name=student.current_class
        )

        db.session.add(payment)

        db.session.commit()

        return jsonify({

            "message":
                "Fees collected successfully",

            "receipt_number":
                receipt_number,

            "student_name":
                student.full_name,

            "amount":
                paid_amount,

            "payment_date":
                str(datetime.now().date()),

            "class_name":
                student.current_class
        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# GET PAYMENTS
@fee_bp.route(
    '/payments',
    methods=['GET']
)
def get_payments():

    try:

        payments = FeePayment.query.all()

        output = []

        for payment in payments:

            student = Student.query.get(
                payment.student_id
            )

            output.append({

                "student_name":
                    student.full_name
                    if student else "",

                "amount":
                    payment.amount,

                "payment_date":
                    payment.payment_date,

                "receipt_number":
                    payment.receipt_number,

                "payment_mode":
                    payment.payment_mode,

                "academic_year":
                    payment.academic_year,

                "class_name":
                    payment.class_name
            })

        return jsonify(output)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500