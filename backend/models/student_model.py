from database.db import db

class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    admission_number = db.Column(db.String(50), unique=True)

    admission_type = db.Column(db.String(20))

    joining_year = db.Column(db.String(20))

    current_class = db.Column(db.String(20))

    section = db.Column(db.String(10))

    parent_name = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    address = db.Column(db.Text)

    bus_required = db.Column(db.Boolean, default=False)

    bus_route = db.Column(db.String(100))

    admission_fee = db.Column(db.Float, default=0)

    tuition_fee = db.Column(db.Float, default=0)

    bus_fee = db.Column(db.Float, default=0)

    old_due = db.Column(db.Float, default=0)

    total_fee = db.Column(db.Float, default=0)

    paid_amount = db.Column(db.Float, default=0)

    remaining_amount = db.Column(db.Float, default=0)

    def __repr__(self):
        return f'<Student {self.full_name}>'