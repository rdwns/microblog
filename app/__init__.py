from flask import Flask
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if not app.debug:

    mailserver = app.config['MAIL_SERVER']
    mailport = app.config['MAIL_PORT']
    mailusername = app.config['MAIL_USERNAME']
    mailpassword = app.config['MAIL_PASSWORD']
    to = app.config['ADMINS']
    usetls = app.config['MAIL_USE_TLS']

    if mailserver:
        auth = None
        if mailusername or mailpassword:
            auth = (mailusername, mailpassword)

        secure = None
        if usetls:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(mailserver, mailport),
            fromaddr='noreply@'+mailserver,
            toaddrs=to,
            subject='App Failure',
            credentials=auth,
            secure=secure
            )
        mail_handler.setLevel(logging.ERROR)

        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors