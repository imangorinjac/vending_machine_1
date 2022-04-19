from model import *


@app.route("/login", methods=["POST"])
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


@app.route("/signup", methods=["POST"])
def register():
    if User.role == "buyer":
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
