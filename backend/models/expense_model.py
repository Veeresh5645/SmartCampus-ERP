from database.db import db

class Expense(db.Model):

    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)

    expense_date = db.Column(db.String(50))

    category = db.Column(db.String(100))

    amount = db.Column(db.Float)

    payment_mode = db.Column(db.String(20))

    comment = db.Column(db.String(300))

    added_by = db.Column(db.String(100))

    academic_year = db.Column(db.String(20))

    def __repr__(self):

        return f'<Expense {self.category}>'