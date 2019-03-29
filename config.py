import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess my secket key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('zhang', 'zhangwei19890518@gmail.com')
    ADMINS = ['zhangwei19890518@gmail.com']

    POSTS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 10

    LANGUAGES = ['en', 'zh']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

    # Admin
    ADMIN_MANAGE_POST_PER_PAGE = 50
    ADMIN_MANAGE_COMMENT_PER_PAGE = 50


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset_password'
    CHANGE_EMAIL = 'change_email'