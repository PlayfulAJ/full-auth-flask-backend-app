from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # bcrypt is a hashing method that allows us to store passwords in a secure way

# this starts the database connection and allows us to use the relational mappper 
db = SQLAlchemy()
bcrypt = Bcrypt()

# modelling all the tables in the database as classes
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True, nullable=False)

    password_hash = db.Column(db.String, nullable=False)

    tasks = db.relationship("Task", back_populates="user")


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)

    description = db.Column(db.Text)

    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship("User", back_populates="tasks")