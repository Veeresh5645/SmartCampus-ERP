from database.db import db

class Expense(db.Model):

    __tablename__ = 'expenses'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    category = db.Column(
        db.String(100)
    )

    amount = db.Column(
        db.Float
    )

    comment = db.Column(
        db.Text
    )

    expense_date = db.Column(
        db.String(50)
    )

    def __repr__(self):

        return f'<Expense {self.category}>'