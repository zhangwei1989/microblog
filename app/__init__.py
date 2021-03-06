import logging
import os
from redis import Redis
import rq

from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app
from config import Config
from elasticsearch import Elasticsearch
from app.extensions import db, migrate, login, mail, bootstrap, moment, babel, ckeditor, csrf, avatars
from app.models import User, Post, Message, Notification, Task, Category, Comment, Role


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_blueprints(app)
    register_extensions(app)
    register_shell_context(app)
    register_logging(app)
    register_template_context(app)

    return app

def register_logging(app):
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    ckeditor.init_app(app)
    csrf.init_app(app)
    avatars.init_app(app)

    from app.api import bp as api_bp
    csrf.exempt(api_bp)


    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

def register_blueprints(app):
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
                'Notification': Notification, 'Task': Task,
                'Category': Category, 'Comment': Comment, 'Role': Role}


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        categories = Category.query.order_by(Category.name).all()
        return dict(categories=categories)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models