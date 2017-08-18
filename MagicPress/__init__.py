# -*- coding:utf-8 -*-
# __author__ = 'huangzp'
import os
from flask import Flask, url_for
from MagicPress.extensions import db, bootstrap, migrate, moment
from flask_admin import Admin, helpers
from flask_admin.contrib import fileadmin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from config import Config, bpdir
from flask_security import Security, SQLAlchemyUserDatastore, utils
from MagicPress.auth.models import User, Role
from MagicPress.auth.admins import UserView, RoleView, BackView
from MagicPress.blog.models import Category, Comment, Article, Tag
from MagicPress.blog.admins import ArticleView, CategoryView, CommentView, TagView, PictureView, MdFileView

path = os.path.join(bpdir, 'static/blog/mdfile')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    # admin.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    admin = Admin(app, u'夜如海洋', base_template='layout.html', template_mode='bootstrap3', index_view=
                  AdminIndexView(
                      name=u'城里 夜如海洋',
                      url='/huangzp',
                      template='admin/index.html'
                  ))

    security = Security(app, user_datastore)

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=helpers,
            get_url=url_for
        )

    from .blog import blog as blog_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(auth_blueprint)


    admin.add_view(RoleView(db.session, name=u'角色'))
    admin.add_view(UserView(db.session, name=u'作者'))
    # admin.add_view(CommentView(db.session, category=u'Blog'))
    admin.add_view(ArticleView(db.session, name=u'文章'))
    admin.add_view(CategoryView(db.session, name=u'分类'))
    admin.add_view(TagView(db.session, name=u'标签'))
    admin.add_view(PictureView(db.session, name=u'配图库'))
    admin.add_view(MdFileView(path, name=u'备份文件'))
    admin.add_view(CommentView(db.session, name=u'评论(coding)'))
    admin.add_view(BackView(name=u"Go Back!"))

    # @app.before_first_request
    # def before_first_request():
    #     user_datastore.find_or_create_role(name='admin', description='Administrator')
    #
    #     encrypted_password = utils.hash_password('password')
    #
    #     if not user_datastore.get_user('admin@example.com'):
    #         user_datastore.create_user(email='admin@example.com', password=encrypted_password)
    #
    #     db.session.commit()
    #
    #     user_datastore.add_role_to_user('admin@example.com', 'admin')
    #     db.session.commit()


    return app
