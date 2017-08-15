import os
from flask_logging

bpdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MagicPress')
basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
ALLOWED_file_EXTENSIONS = set(['md', 'MD', 'word', 'txt', 'py', 'java', 'c', 'c++', 'xlsx'])
ALLOWED_photo_EXTENSIONS = set(['png', 'jpg', 'xls', 'JPG', 'PNG', 'gif', 'GIF'])
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i am cool'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    #SQLALCHEMY_DATABASE_URI = 'mysql://root:Renderg@123@127.0.0.1:3306/magicpress'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


    server_log = TimedRotatingFileHandler('server.log', 'D')
    server_log.setLevel(logging.DEBUG)
    server_log.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))

    error_log = TimedRotatingFileHandler('error.log', 'D')
    error_log.setLevel(logging.ERROR)
    error_log.setFormatter(logging.Formatter(
        '%(asctime)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    app.logger.addHandler(server_log)
    app.logger.addHandler(error_log)
    @staticmethod
    def init_app(app):
        pass