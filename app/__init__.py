import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from elasticsearch import Elasticsearch
from flask_uploads import UploadSet, IMAGES, configure_uploads
from config import Config
#
app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
mail = Mail(app)
#
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# configure img uploads via flask-uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)


from app import routes, models, errors


def creat_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#             secure = None
#             if app.config['MAIL_USE_TLS']:
#                 secure = ()
#             mail_handler = SMTPHandler(
#                 mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#                 fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#                 toaddrs=app.config['ADMINS'], subject='Ticket System Failure',
#                 credentials=auth, secure=secure
#             )
#             mail_handler.setlevel(logging.ERROR)
#             app.logger.addHandler(mail_handler)
# # #             # logging of file based log
#             if not os.path.exists('logs'):
#                 os.mkdir('logs')
#             file_handler = RotatingFileHandler('logs/system.log', maxBytes=10240, backupCount=10)
#             file_handler.setFormatter(logging.Formatter(
#                 '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
#             ))
#             file_handler.setLevel(logging.INFO)
#             app.logger.addHandler(file_handler)
#
#             app.logger.setLevel(logging.INFO)
#             app.logger.info('Ticket System startup')

#
# # from app import models
