from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from models import Cupcake, Order, CupcakeOrder, Customer, FavoriteCupcake


class FavoriteCupcakeSchema(SQLAlchemySchema):
    class Meta:
        model = FavoriteCupcake
        load_instance = True

    id = auto_field()
    customer_id = auto_field()
    cupcake_id = auto_field()


class CupcakeSchema(SQLAlchemySchema):
    class Meta:
        model = Cupcake
        load_instance = True

    id = auto_field()
    name = auto_field()
    price = auto_field()


class CustomerSchema(SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True

    id = auto_field()
    username = auto_field()
    name = auto_field()


class CupcakeOrderSchema(SQLAlchemySchema):
    class Meta:
        model = CupcakeOrder
        load_instance = True

    id = auto_field()
    order_id = auto_field()
    cupcake_id = auto_field()
    quantity = auto_field()


class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True

    id = auto_field()
    customer_id = auto_field()
    total_amount = auto_field()
    customer = auto_field()

    cupcakes = Nested(CupcakeOrderSchema, many=True)
