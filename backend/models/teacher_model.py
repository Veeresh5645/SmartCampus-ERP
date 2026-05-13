from database.db import db

class Teacher(db.Model):

    __tablename__ = 'teachers'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(200)
    )

    email = db.Column(
        db.String(200)
    )

    phone = db.Column(
        db.String(50)
    )

    subject = db.Column(
        db.String(100)
    )

    salary = db.Column(
        db.Integer,
        default=0
    )

    def __repr__(self):

        return f'<Teacher {self.full_name}>'