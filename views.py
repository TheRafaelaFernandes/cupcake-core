from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Cupcake, CupcakeOrder, Order, Customer, FavoriteCupcake
from serializer import CupcakeSchema, CupcakeOrderSchema, OrderSchema, CustomerSchema, FavoriteCupcakeSchema


class BaseView(MethodView):
    model = None
    schema = None

    def get(self, id=None):
        if id:
            instance = self.model.query.get_or_404(id)
            return jsonify(self.schema.dump(instance))
        instances = self.model.query.all()
        return jsonify(self.schema.dump(instances, many=True))

    def post(self):
        data = request.get_json()
        instance = self.model(**data)
        db.session.add(instance)
        db.session.commit()
        return jsonify(self.schema.dump(instance)), 201

    def put(self, id):
        instance = self.model.query.get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(instance, key, value)
        db.session.commit()
        return jsonify(self.schema.dump(instance))

    def delete(self, id):
        instance = self.model.query.get_or_404(id)
        try:
            db.session.delete(instance)
            db.session.commit()
            return jsonify({"message": "Excluído com sucesso"}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Erro de integridade ao excluir"}), 400

class FavoriteCupcakeView(BaseView):
    model = FavoriteCupcake
    schema = FavoriteCupcakeSchema()

    def post(self):
        data = request.get_json()
        customer_id = data.get("customer_id")
        cupcake_id = data.get("cupcake_id")

        existing_favorite = FavoriteCupcake.query.filter_by(customer_id=customer_id, cupcake_id=cupcake_id).first()

        if existing_favorite:
            db.session.delete(existing_favorite)
            db.session.commit()
            return jsonify({"message": "Removido dos favoritos"}), 200

        favorite = FavoriteCupcake(customer_id=customer_id, cupcake_id=cupcake_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({"message": "Adicionado aos favoritos"}), 201


class CupcakeView(BaseView):
    model = Cupcake
    schema = CupcakeSchema()

    def post(self):
        data = request.get_json()

        try:
            instance = self.model(**data)
            db.session.add(instance)
            db.session.commit()
            return jsonify(self.schema.dump(instance)), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "error"}), 400


class CustomerView(BaseView):
    model = Customer
    schema = CustomerSchema()

    def post(self):
        data = request.get_json()

        try:
            instance = self.model(**data)
            db.session.add(instance)
            db.session.commit()
            return jsonify(self.schema.dump(instance)), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Usuário já existe"}), 400


class OrderView(BaseView):
    model = Order
    schema = OrderSchema()

    def post(self):
        data = request.get_json()

        try:
            order = Order(
                customer_id=data["customer_id"],
                total_amount=data["total_amount"]
            )
            db.session.add(order)
            db.session.flush()

            for cupcake in data["cupcakes"]:
                existing_cupcake = Cupcake.query.get(cupcake["id"])
                if not existing_cupcake:
                    raise ValueError(f"Cupcake com ID {cupcake['id']} não encontrado.")

                cupcake_order = CupcakeOrder(
                    order_id=order.id,
                    cupcake_id=existing_cupcake.id,
                    quantity=cupcake["quantity"]
                )
                db.session.add(cupcake_order)

            db.session.commit()
            return jsonify({"message": "Pedido criado com sucesso", "order_id": order.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Erro ao criar pedido", "details": str(e)}), 400



class CupcakeOrderView(BaseView):
    model = CupcakeOrder
    schema = CupcakeOrderSchema()

    def get(self):
        customer_id = request.args.get('customer_id')  # Filtrar por cliente (opcional)

        # Realiza o join para obter os dados expandidos
        query = db.session.query(
            CupcakeOrder,
            Order,
            Cupcake
        ).join(Order, CupcakeOrder.order_id == Order.id)\
         .join(Cupcake, CupcakeOrder.cupcake_id == Cupcake.id)

        if customer_id:
            query = query.filter(Order.customer_id == customer_id)

        results = query.all()

        # Formatar a resposta com dados expandidos
        expanded_results = [
            {
                "cupcake_order": self.schema.dump(cupcake_order),
                "order": {
                    "id": order.id,
                    "customer_id": order.customer_id,
                    "total_amount": order.total_amount
                },
                "cupcake": {
                    "id": cupcake.id,
                    "name": cupcake.name,
                    "price": cupcake.price
                }
            }
            for cupcake_order, order, cupcake in results
        ]

        return jsonify(expanded_results)


class LoginView(MethodView):
    @staticmethod
    def post():
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"erro": "Username e senha são obrigatórios"}), 400

            customer = Customer.query.filter_by(username=username).first()

            if customer and customer.password == password:
                return jsonify(customer.as_dict())
            else:
                return jsonify({"customer_id": None})
        except Exception as e:
            return jsonify({"erro": "Erro no servidor", "detalhes": str(e)}), 500
