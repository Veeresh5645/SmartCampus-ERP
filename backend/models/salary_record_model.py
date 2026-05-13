from database.db import db

class SalaryRecord(db.Model):

    __tablename__ = 'salary_records'

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer)

    teacher_name = db.Column(db.String(100))

    month = db.Column(db.String(30))

    total_working_days = db.Column(db.Integer)

    attended_days = db.Column(db.Integer)

    monthly_salary = db.Column(db.Float)

    calculated_salary = db.Column(db.Float)

    def __repr__(self):

        return f'<SalaryRecord {self.teacher_name}>'