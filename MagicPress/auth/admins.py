# -*- coding: utf-8 -*-
from .models import Author
from MagicPress.blog.admins import BaseBlogView

class AuthorView(BaseBlogView):

    column_list = ['id', 'name', 'categories', 'tags', 'comments', 'articles']

    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        'id': u'序号',
        'name': u'名字',
        'categories': u'类别',
        'tags': u'标签',
        'comments': u'评论',
        'articles': u'文章'
    }

    def __init__(self, session, **kwargs):
        super(AuthorView, self).__init__(Author, session, **kwargs)
