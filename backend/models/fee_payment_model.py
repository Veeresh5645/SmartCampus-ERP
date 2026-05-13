from database.db import db

class FeePayment(db.Model):

    __tablename__ = 'fee_payments'

    id = db.Column(db.Integer, primary_key=True)

    receipt_number = db.Column(db.String(50))

    student_name = db.Column(db.String(100))

    admission_number = db.Column(db.String(50))

    academic_year = db.Column(db.String(20))

    class_name = db.Column(db.String(50))

    amount_paid = db.Column(db.Float)

    payment_mode = db.Column(db.String(20))

    transaction_id = db.Column(db.String(100))

    collected_by = db.Column(db.String(100))

    payment_date = db.Column(db.String(50))

    def __repr__(self):

        return f'<FeePayment {self.receipt_number}>'