from flask import session
from model import *


@app.route("/deposit")
def deposit(coins):
    if User.role == "buyer":
        coin_list = [5, 10, 20, 50, 100]
        username = session["username"]
        user = User.query.get(id)
        if coins in coin_list:
            user.deposit += coins
    else:
        return 401
    return deposit(coins)


@app.route("/buy")
def buy(id, amountAvailable):
    username = session["username"]
    user = User.query.get(username)
    if user.role != "buyer":
        return 401
    product = Product.query.get(id)
    if Product.amountAvailable < 1:
        return "no products available"
    total_cost = Product.cost * amountAvailable
    if total_cost > user.deposit():
        return 400, "deposit more coins"
