from database.db import db

class TeacherAttendance(db.Model):

    __tablename__ = 'teacher_attendance'

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer)

    teacher_name = db.Column(db.String(100))

    attendance_date = db.Column(db.String(50))

    status = db.Column(db.String(20))

    def __repr__(self):

        return f'<TeacherAttendance {self.teacher_name}>'