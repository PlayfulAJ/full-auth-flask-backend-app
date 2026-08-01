from flask import Flask
from flask_migrate import Migrate # the migrate allows us to make changes to the database without losing data
from flask_jwt_extended import JWTManager #JWT is a method of authentication that allows us to create secure tokens for users to acceess protected routes

from models import db, bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "the-secret-key"

db.init_app(app)
bcrypt.init_app(app)

jwt = JWTManager(app)

migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(port=5555, debug=True)