from flask import Flask
import logging
from logging.handlers import SMTPHandler
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

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

from app import routes, models, errors