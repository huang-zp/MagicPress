# -*- coding:utf-8 -*-
# __author__ = 'huangzp'
import os
from flask import Flask
from MagicPress.extensions import db, bootstrap, migrate, moment
from flask_admin import Admin
from flask_admin.contrib import fileadmin
from flask_admin.contrib.sqla import ModelView
from config import Config, bpdir
from MagicPress.auth.models import User
from MagicPress.auth.admins import UserView
from MagicPress.blog.models import Category, Comment, Article, Tag
from MagicPress.blog.admins import ArticleView, CategoryView, CommentView, TagView, PictureView

path = os.path.join(bpdir, 'static/blog/mdfile')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    # admin.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    admin = Admin(app, u'夜如海洋', base_template='layout.html', template_mode='bootstrap3')
    from .blog import blog as blog_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(auth_blueprint)
    admin.add_view(UserView(db.session, name=u'作者'))
    # admin.add_view(CommentView(db.session, category=u'Blog'))
    admin.add_view(ArticleView(db.session, name=u'文章'))
    admin.add_view(CategoryView(db.session, name=u'分类'))
    admin.add_view(TagView(db.session, name=u'标签'))
    admin.add_view(PictureView(db.session, name=u'配图库'))
    admin.add_view(fileadmin.FileAdmin(path, name=u'备份文件'))
    admin.add_view(CommentView(db.session, name=u'评论(coding)'))

    return app
