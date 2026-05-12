from database.db import db

class Attendance(db.Model):

    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)

    student_name = db.Column(db.String(100))

    class_name = db.Column(db.String(20))

    date = db.Column(db.String(50))

    status = db.Column(db.String(20))

    def __repr__(self):
        return f'<Attendance {self.student_name}>'