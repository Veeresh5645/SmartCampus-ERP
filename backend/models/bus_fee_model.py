from database.db import db

class BusFee(db.Model):

    __tablename__ = 'bus_fees'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    route_name = db.Column(
        db.String(100)
    )

    bus_fee = db.Column(
        db.Float,
        default=0
    )

    def __repr__(self):

        return f'<BusFee {self.route_name}>'