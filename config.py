import os


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

    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'

    SECURITY_PASSWORD_SALT = 'xxxxxxxxxxxxxxxxx'


    SECURITY_URL_PREFIX = "/huangzp"

    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/huangzp/"
    SECURITY_POST_LOGOUT_VIEW = "/huangzp/"
    SECURITY_POST_REGISTER_VIEW = "/huangzp/"
    THEME = "blog"

    @staticmethod
    def init_app(app):
        pass