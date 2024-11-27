from flask import Blueprint, jsonify, current_app, request

from extensions import db
from models import Cupcake, FavoriteCupcake
from serializer import CupcakeSchema
from views import CupcakeView, CustomerView, LoginView, CupcakeOrderView, OrderView, FavoriteCupcakeView

bp = Blueprint("routes", __name__)

bp.add_url_rule("/favorite_cupcake", view_func=FavoriteCupcakeView.as_view("favorite_cupcake"), methods=["POST", "DELETE"])

bp.add_url_rule("/cupcakes", view_func=CupcakeView.as_view("cupcake_list"), methods=["POST"])
bp.add_url_rule("/cupcakes/<int:id>", view_func=CupcakeView.as_view("cupcake_detail"), methods=["PUT", "DELETE"])

bp.add_url_rule("/customer", view_func=CustomerView.as_view("customer_list"), methods=["GET", "POST"])
bp.add_url_rule("/customer/<int:id>", view_func=CustomerView.as_view("customer_detail"), methods=["GET", "PUT", "DELETE"])

bp.add_url_rule("/order", view_func=OrderView.as_view("order_list"), methods=["GET", "POST"])
bp.add_url_rule("/order/<int:id>", view_func=OrderView.as_view("order_detail"), methods=["GET", "PUT", "DELETE"])

bp.add_url_rule("/cupcake_order", view_func=CupcakeOrderView.as_view("cupcake_order_list"), methods=["GET", "POST"])
bp.add_url_rule("/cupcake_order/<int:id>", view_func=CupcakeOrderView.as_view("cupcake_order_detail"), methods=["GET", "PUT", "DELETE"])

bp.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])

@bp.route('/cupcakes', methods=['GET'])
def get_cupcakes():
    customer_id = request.args.get('customer_id', type=int)
    cupcakes = Cupcake.query.all()

    favorite_cupcakes = []
    if customer_id:
        favorite_cupcakes = {fav.cupcake_id for fav in FavoriteCupcake.query.filter_by(customer_id=customer_id).all()}

    schema = CupcakeSchema(many=True)
    cupcakes_data = schema.dump(cupcakes)
    for cupcake in cupcakes_data:
        cupcake["is_favorite"] = cupcake["id"] in favorite_cupcakes

    return jsonify(cupcakes_data)

@bp.route('/favorite_cupcake', methods=['GET'])
def get_favorite_cupcake():
    customer_id = request.args.get('customer_id', type=int)

    if not customer_id:
        return jsonify({"error": "O parâmetro customer_id é obrigatório"}), 400

    favorite_cupcakes = (
        db.session.query(FavoriteCupcake, Cupcake)
        .join(Cupcake, FavoriteCupcake.cupcake_id == Cupcake.id)
        .filter(FavoriteCupcake.customer_id == customer_id)
        .all()
    )

    favorite_list = [
        {
            "name": cupcake.name,
            "price": cupcake.price
        }
        for fav, cupcake in favorite_cupcakes
    ]

    return jsonify(favorite_list), 200



@bp.route("/", methods=["GET"])
def index():
    routes = []
    for rule in current_app.url_map.iter_rules():
        methods = ",".join(rule.methods)
        routes.append({"endpoint": rule.endpoint, "methods": methods, "url": str(rule)})

    return jsonify({"routes": routes})
