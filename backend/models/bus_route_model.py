from database.db import db

class BusRoute(db.Model):

    __tablename__ = 'bus_routes'

    id = db.Column(db.Integer, primary_key=True)

    route_name = db.Column(db.String(100))

    bus_fee = db.Column(db.Float)

    def __repr__(self):

        return f'<BusRoute {self.route_name}>'