from database.db import db

class SalaryRecord(db.Model):

    __tablename__ = 'salary_records'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    teacher_id = db.Column(
        db.Integer
    )

    month = db.Column(
        db.String(50)
    )

    working_days = db.Column(
        db.Integer,
        default=0
    )

    attended_days = db.Column(
        db.Integer,
        default=0
    )

    calculated_salary = db.Column(
        db.Float,
        default=0
    )

    is_paid = db.Column(
        db.Boolean,
        default=False
    )

    payment_mode = db.Column(
        db.String(50)
    )

    paid_date = db.Column(
        db.String(50)
    )

    def __repr__(self):

        return f'<SalaryRecord {self.teacher_id}>'