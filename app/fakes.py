import random

from faker import Faker
from app import db
from app.models import Category, Post, User
from sqlalchemy.exc import IntegrityError


fake = Faker('zh')


def fake_users(count=5):
    for i in range(count):
        user = User(username=fake.name(), email=fake.email())
        user.set_password(fake.password())
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_categories(count=10):
    category = Category(name='默认')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    users = User.query.all()
    for user in users:
        for i in range(count):
            ids = [x for x, in db.session.query(Category.id).all()]
            post = Post(
                title=fake.sentence(5),
                body=fake.text(2000),
                author=user,
                category=Category.query.get(random.choice(ids)),
                timestamp=fake.date_time_this_year(),
                language='zh'
            )
            db.session.add(post)

    db.session.commit()
