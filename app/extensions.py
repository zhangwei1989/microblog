from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from flask_avatars import Avatars


db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
ckeditor = CKEditor()
csrf = CSRFProtect()
avatars = Avatars()

class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False

login.anonymous_user = Guest