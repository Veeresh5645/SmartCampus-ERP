from database.db import db

class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(200)
    )

    admission_number = db.Column(
        db.String(100),
        unique=True
    )

    admission_type = db.Column(
        db.String(50)
    )

    joining_year = db.Column(
        db.String(50)
    )

    academic_year = db.Column(
        db.String(50)
    )

    current_class = db.Column(
        db.String(100)
    )

    section = db.Column(
        db.String(50)
    )

    parent_name = db.Column(
        db.String(200)
    )

    phone = db.Column(
        db.String(50)
    )

    address = db.Column(
        db.Text
    )

    bus_required = db.Column(
        db.Boolean,
        default=False
    )

    bus_route = db.Column(
        db.String(200)
    )

    total_fee = db.Column(
        db.Integer,
        default=0
    )

    paid_amount = db.Column(
        db.Integer,
        default=0
    )

    remaining_amount = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):

        return f'<Student {self.full_name}>'