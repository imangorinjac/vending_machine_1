from model import *

app = Flask(__name__)


@app.route("/product", methods=["POST"])  # create a product
def add_product():
    if User.role == "seller":
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
    if User.role == "seller":
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
    if User.role == "seller":
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
    return product_schema.jsoinfy(product)


if __name__ == "__main__":
    app.run(debug=True)
