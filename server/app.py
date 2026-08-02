from flask import Flask, request, make_response
from flask_migrate import Migrate # the migrate allows us to make changes to the database without losing data
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity #JWT is a method of authentication that allows us to create secure tokens for users to acceess protected routes

from models import db, bcrypt, User, Task

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////mnt/c/Users/jabar/Moringa/full-auth-flask-backend-app/server/instance/app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "this_is_a_secret_key"

db.init_app(app)
bcrypt.init_app(app)

jwt = JWTManager(app)

migrate = Migrate(app, db)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        username=data["username"],
        password_hash=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return make_response({
        "id": user.id,
        "username": user.username
    }, 201)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(
        username=data["username"]
    ).first()

    if user is None:
        return make_response(
            {"error": "Invalid username or password"},
            401
        )

    if not bcrypt.check_password_hash(
        user.password_hash,
        data["password"]
    ):
        return make_response(
            {"error": "Invalid username or password"},
            401
        )

    access_token = create_access_token(
        identity=str(user.id)
    )

    return make_response(
        {
            "access_token": access_token
        },
        200
    )

@app.route("/me", methods=["GET"])
@jwt_required()
def me():

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if user is None:
        return make_response(
            {"error": "User not found"},
            404
        )

    return make_response(
        {
            "id": user.id,
            "username": user.username
        },
        200
    )

if __name__ == "__main__":
    app.run(port=5555, debug=True)