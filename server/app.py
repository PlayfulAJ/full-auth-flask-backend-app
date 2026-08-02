from flask import Flask, request, make_response
from flask_migrate import Migrate # the migrate allows us to make changes to the database without losing data
from flask_jwt_extended import JWTManager #JWT is a method of authentication that allows us to create secure tokens for users to acceess protected routes

from models import db, bcrypt, User, Task

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////mnt/c/Users/jabar/Moringa/full-auth-flask-backend-app/server/instance/app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "the-secret-key"

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


if __name__ == "__main__":
    app.run(port=5555, debug=True)