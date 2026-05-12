from database.db import db

class Teacher(db.Model):

    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100))

    subject = db.Column(db.String(100))

    salary = db.Column(db.Float, default=0)

    paid_salary = db.Column(db.Float, default=0)

    remaining_salary = db.Column(db.Float, default=0)

    def __repr__(self):
        return f'<Teacher {self.full_name}>'