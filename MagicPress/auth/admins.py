# -*- coding: utf-8 -*-
from .models import User, Role
from MagicPress.blog.admins import BaseBlogView
from flask_security import current_user
from flask import abort, redirect, request, url_for
from flask_admin import BaseView, expose


class UserView(BaseBlogView):

    column_list = ['id', 'name', 'email', 'roles', 'articles']

    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        'id': u'序号',
        'name': u'名字',
        'email': u'邮箱',
        'roles': u'角色',
        'articles': u'文章'
    }

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


class RoleView(BaseBlogView):

    column_list = ['id', 'name', 'description']

    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        'id': u'序号',
        'name': u'角色',
        'description': u'描述'
    }

    def __init__(self, session, **kwargs):
        super(RoleView, self).__init__(Role, session, **kwargs)


class BackView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('blog.index'))