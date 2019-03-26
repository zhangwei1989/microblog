import click
from app import db
from app.models import User, Post


def register(app):
    @app.cli.command()
    @click.option('--count', default=20, help='Quantity of posts, default is 20.')
    def forge(count):
        """Generate fake posts for every user."""
        from faker import Faker

        faker = Faker()
        click.echo('Generating data...')

        users = User.query.all()
        for user in users:
            for i in range(count):
                post = Post(
                    title=faker.sentence(5),
                    body=faker.text(2000),
                    author=user,
                    timestamp=faker.date_time_this_year(),
                    language='zh'
                )
                db.session.add(post)

        db.session.commit()
        click.echo('Completed')
