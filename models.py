from extensions import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    superuser = db.Column(db.Boolean, default=False)

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("password", None)
        return data

class Cupcake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class CupcakeOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    cupcake_id = db.Column(db.Integer, db.ForeignKey('cupcake.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('order', lazy=True))
    cupcakes = db.relationship('CupcakeOrder', backref='order', lazy=True)
    total_amount = db.Column(db.Float, nullable=False)

class FavoriteCupcake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    cupcake_id = db.Column(db.Integer, db.ForeignKey('cupcake.id'), nullable=False)

