from app import app
from models import db, bcrypt, User, Task

with app.app_context():
    Task.query.delete()
    User.query.delete()

    user1 = User(
        username="john",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
    )

    user2 = User(
        username="patrick",
        password_hash=bcrypt.generate_password_hash("password321").decode("utf-8")
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    task1 = Task(
        title="Homework",
        description="Write an french essay",
        completed=False,
        user_id=user1.id
    )

    task2 = Task(
        title="Study History",
        description="Read about the human evolution",
        completed=False,
        user_id=user1.id
    )

    task3 = Task(
        title="Go Gym",
        description="Leg day",
        completed=True,
        user_id=user2.id
    )

    db.session.add_all([
        task1,
        task2,
        task3
    ])

    db.session.commit()

    print("seed data added successfully!")