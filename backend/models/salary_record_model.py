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

    salary = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):

        return f'<SalaryRecord {self.teacher_id}>'