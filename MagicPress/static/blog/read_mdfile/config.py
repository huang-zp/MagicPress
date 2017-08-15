import os

bpdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'MagicPress')
basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i am cool'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    #SQLALCHEMY_DATABASE_URI = 'mysql://root:Renderg@123@127.0.0.1:3306/magicpress'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass