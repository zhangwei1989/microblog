import random

from faker import Faker
from app import db
from app.models import Category, Post, User, Comment
from sqlalchemy.exc import IntegrityError


fake = Faker('zh')


def fake_admin(username, email, password):
    admin = User(username=username, email=email, is_admin=True)
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()


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


def fake_posts(count=20):
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


def fake_comments(count=10):
    posts = Post.query.all()
    for post in posts:
        # 创建游客的留言
        for i in range(count):
            comment = Comment(author=fake.name(), email=fake.email(),
                              body=fake.sentence(), post=post,
                              timestamp=fake.date_time_this_year())
            db.session.add(comment)

        # 创建隐藏的留言
        for i in range(count):
            comment = Comment(author=fake.name(), email=fake.email(),
                              body=fake.sentence(), post=post, is_hidden=True,
                              timestamp=fake.date_time_this_year())
            db.session.add(comment)

        # 创建作者的留言
        for i in range(count):
            comment = Comment(author=post.author.username, email=post.author.email,
                              body=fake.sentence(), post=post, from_post_author=True,
                              timestamp=fake.date_time_this_year())
            db.session.add(comment)

    # 创建回复其他回复的留言
    comment_ids = [x for x, in db.session.query(Comment.id)]
    for i in range(count * 100):
        replied = Comment.query.get(random.choice(comment_ids))

        if replied.is_hidden:
            continue
        comment = Comment(author=fake.name(), email=fake.email(),
                          body=fake.sentence(), post=replied.post,
                          replied=replied,
                          timestamp=fake.date_time_between_dates(datetime_start=replied.timestamp))
        db.session.add(comment)

    db.session.commit()



