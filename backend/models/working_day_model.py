from database.db import db

class WorkingDay(db.Model):

    __tablename__ = 'working_days'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    attendance_date = db.Column(
        db.String(50)
    )

    is_working_day = db.Column(
        db.Boolean
    )

    holiday_reason = db.Column(
        db.String(200)
    )

    def __repr__(self):

        return f'<WorkingDay {self.attendance_date}>'