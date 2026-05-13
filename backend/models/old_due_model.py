from database.db import db

class OldDue(db.Model):

    __tablename__ = 'old_dues'

    id = db.Column(db.Integer, primary_key=True)

    student_admission_number = db.Column(db.String(50))

    academic_year = db.Column(db.String(20))

    pending_fee = db.Column(db.Float)

    def __repr__(self):

        return f'<OldDue {self.academic_year}>'