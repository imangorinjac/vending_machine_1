from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import os
import uuid
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
migrate = Migrate(app, db)
ma = Marshmallow(app)


class User(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, role, **kwargs):
        self.username = username
        self.password = password
        self.role = role


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "role")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Product(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    amountAvailable = db.Column(db.String(80), unique=True, nullable=False)
    cost = db.Column(db.String(120), nullable=False)
    productName = db.Column(db.String(120), nullable=False)

    def __init__(self, amountAvaiable, cost, productName, **kwargs):
        self.amountAvaiable = amountAvaiable
        self.cost = cost
        self.productName = productName


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("sellerid", "amountAvailable", "cost", "productName")


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

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


if __name__ == "__main__":
    app.run(debug=True)
