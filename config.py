import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'dom.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
#     ITEMS_PER_PAGE = 10
    TICKETS_PER_PAGE = 10
#     WHOOSH_BASE = 'whoosh'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
#     # config for emails
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'todayy06@gmail.com'
    MAIL_PASSWORD = '0416676504'
    ADMINS = ['todayy06@gmail.com']

    # img uploads
    UPLOADS_DEFAULT_DEST = '/app/static/img'            # TOP_LEVEL_DIR +
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img'

    UPLOADED_DEFAULT_DEST = '/app/static/img'
    UPLOADED_DEFAULT_URL = 'http://localhost:5000/static/img'


#
