from database.db import db

class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100)
    )

    admission_number = db.Column(
        db.String(100)
    )

    current_class = db.Column(
        db.String(50)
    )

    academic_year = db.Column(
        db.String(50)
    )

    bus_required = db.Column(
        db.String(10)
    )

    bus_route = db.Column(
        db.String(100)
    )

    total_fees = db.Column(
        db.Float,
        default=0
    )

    paid_amount = db.Column(
        db.Float,
        default=0
    )

    remaining_amount = db.Column(
        db.Float,
        default=0
    )

    def __repr__(self):

        return f'<Student {self.full_name}>'