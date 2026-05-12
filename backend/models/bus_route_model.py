from database.db import db

class BusRoute(db.Model):

    __tablename__ = 'bus_routes'

    id = db.Column(db.Integer, primary_key=True)

    route_name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    bus_fee = db.Column(db.Float, default=0)

    def __repr__(self):
        return f'<BusRoute {self.location}>'