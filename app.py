from flask import Flask, jsonify, request, make_response
from sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.registration"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class User(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "role")


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)


class Product(db.Model):
    __table_args__ = {"extend_existing": True}
    sellerid = db.Column(db.Integer, primary_key=True)
    amountAvailable = db.Column(db.String(80), unique=True, nullable=False)
    cost = db.Column(db.String(120), nullable=False)
    productName = db.Column(db.String(120), nullable=False)

    def __init__(self, amountAvaiable, cost, productName):
        self.amountAvaiable = amountAvaiable
        self.cost = cost
        self.productName = productName


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("sellerid", "amountAvailable", "cost", "productName")


product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

db.create_all()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid !!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/user", methods=["GET"])  # get the user
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        output.append(
            {"username": user.username, "password": user.password, "role": user.role}
        )

    return jsonify({"users": output})


@app.route("/user/<id>", methods=["DELETE"])  # delete a certain user
@token_required
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsoinfy(user)


@app.route("/user/<id>", methods=["PUT"])  # update the user
@token_required
def update_user(id):
    user = User.query.get(id)
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    user.username = username
    user.password = password
    user.role = role
    db.session.commit()
    return user_schema.jsonify(user)


@app.route("/signup", methods=["POST"])
def register():
    data = request.form
    username, password = data.get("username"), data.get("password")
    role = data.get("role")
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        user = User(
            username=username, password=generate_password_hash(password), role=role
        )
        db.session.add(user)
        db.session.commit()

        return make_response("Successfully registered.", 201)
    else:
        return make_response("User already exists. Please Log in.", 202)


def login():
    auth = request.form
    if not auth or not auth.get("username") or not auth.get("password"):

        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm ="Login required !!"'},
        )

    user = User.query.filter_by(username=auth.get("username")).first()

    if not user:
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm ="User does not exist !!"'},
        )

    if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "exp": datetime.utcnow() + timedelta(hours=24),
            },
            app.config["SECRET_KEY"],
        )

        return make_response(jsonify({"token": token.decode("UTF-8")}), 201)
    return make_response(
        "Could not verify",
        403,
        {"WWW-Authenticate": 'Basic realm ="Wrong Password !!"'},
    )


@app.route("/product", methods=["POST"])  # create a product
def add_product():

    amountAvailable = request.json["amountAvailable"]
    cost = request.json["cost"]
    productName = request.json["productName"]
    new_product = Product(amountAvailable, cost, productName)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


@app.route("/products", methods=["GET"])  # get the list of all the products
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)


@app.route("/product/<id>", methods=["GET"])  # search for the one you are looking for
def get_products():
    product = Product.query.get(id)
    return product_schema.jsoinfy(product)


@app.route("/product/<id>", methods=["PUT"])  # update the product
def update_product(id):
    product = Product.query.get(id)
    amountAvailable = request.json["amountAvailable"]
    cost = request.json["cost"]
    productName = request.json["productName"]
    product.amountAvailable = amountAvailable
    product.cost = cost
    product.productName = productName
    db.session.commit()
    return product_schema.jsonify(product)


@app.route("/product/<id>", methods=["DELETE"])  # delete a certain product
def delete_products(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsoinfy(product)


if __name__ == "__main__":
    app.run(debug=True)
