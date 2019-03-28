import click
from app import db


def register(app):
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--email', prompt=True, help='The email.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, email, password):
        """Init Database, and generate admin."""
        from app.fakes import fake_admin

        click.echo('Initing database...')
        db.drop_all()
        db.create_all()

        click.echo('Generating admin...')
        fake_admin(username, email, password)

        click.echo('Completed')

    @app.cli.command()
    @click.option('--count', default=20, help='Quantity of posts, default is 20.')
    def forge(count):
        """Generate fake posts for every user."""
        from app.fakes import fake_users, fake_categories, fake_posts, fake_comments

        click.echo('Generating user...')
        fake_users()

        click.echo('Generating category...')
        fake_categories()

        click.echo('Generating post...')
        fake_posts()

        click.echo('Generating comment...')
        fake_comments()

        click.echo('Completed')
