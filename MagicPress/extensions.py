# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_migrate import Migrate
from flask_moment import Moment
from flask_cache import Cache


db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
moment = Moment()
cache = Cache()
