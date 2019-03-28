import click


def register(app):
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
