from model import *


@app.route("/user", methods=["POST"])  # create user
def add_user():

    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    new_user = User(username, password, role)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


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
