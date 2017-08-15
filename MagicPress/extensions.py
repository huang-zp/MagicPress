# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_migrate import Migrate


db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
