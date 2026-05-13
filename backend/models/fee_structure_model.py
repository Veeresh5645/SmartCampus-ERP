from database.db import db

class FeeStructure(db.Model):

    __tablename__ = 'fee_structures'

    id = db.Column(db.Integer, primary_key=True)

    academic_year = db.Column(db.String(20))

    class_name = db.Column(db.String(50))

    tuition_fee = db.Column(db.Float)

    new_admission_fee = db.Column(db.Float)

    old_admission_fee = db.Column(db.Float)

    def __repr__(self):

        return f'<FeeStructure {self.class_name}>'