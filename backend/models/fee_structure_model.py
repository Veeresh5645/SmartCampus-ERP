from database.db import db

class FeeStructure(db.Model):

    __tablename__ = 'fee_structures'

    id = db.Column(db.Integer, primary_key=True)

    class_name = db.Column(db.String(50), nullable=False)

    admission_fee = db.Column(db.Float, default=0)

    tuition_fee = db.Column(db.Float, default=0)

    is_bus_available = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<FeeStructure {self.class_name}>'