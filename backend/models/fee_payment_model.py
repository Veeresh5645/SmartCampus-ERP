from database.db import db

class FeePayment(db.Model):

    __tablename__ = 'fee_payments'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer
    )

    amount = db.Column(
        db.Float
    )

    payment_date = db.Column(
        db.String(50)
    )

    receipt_number = db.Column(
        db.String(100)
    )

    payment_mode = db.Column(
        db.String(50)
    )

    academic_year = db.Column(
        db.String(50)
    )

    class_name = db.Column(
        db.String(50)
    )

    def __repr__(self):

        return f'<FeePayment {self.receipt_number}>'