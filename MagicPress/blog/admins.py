# -*- coding: utf-8 -*-
import json
import os
import time
import codecs
from datetime import date
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request, current_app, url_for, abort
from .models import Article, Category, Comment, Tag, Picture
from flask_admin import expose, form
from .forms import ArticleForm
from MagicPress.extensions import db
from config import bpdir, ALLOWED_file_EXTENSIONS, ALLOWED_photo_EXTENSIONS
from werkzeug.utils import secure_filename
from flask_admin.model.template import macro
from sqlalchemy.event import listens_for
from jinja2 import Markup
from flask_security import current_user
from flask_admin.contrib import fileadmin


def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_photo_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_file_EXTENSIONS


class BaseBlogView(ModelView):

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        if current_user.has_role('admin'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

    list_template = 'list.html'
    create_template = 'blog_create.html'
    edit_template = 'edit.html'

    can_edit = True
    can_delete = True
    can_view_details = True


class ArticleView(BaseBlogView):

    list_template = '_article_list.html'
    edit_template = '_edit_get_form.html'
    # column_exclude_list = ['abstract', 'text', 'comments']

    column_list = ['id', 'photo', 'abstract', 'title', 'text', 'create_time', 'update_time', 'state', 'category_id',
                   'visit_num', 'category', 'tags', 'comments', 'user_id', 'picture']

    column_searchable_list = ['title']
    column_filters = ['title', 'create_time', 'state']

    form_excluded_columns = ['title', 'text']

    # 覆盖path默认显示
    def _list_thumbnail(view, context, model, name):
        if not model.picture or not model.picture.path:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename='blog/picture/' + 'thumb-' + model.picture.path))

    column_formatters = dict(text=macro('render_text'), abstract=macro('render_abstract'), picture=_list_thumbnail)





    column_labels = {
        'id': u'序号',
        'photo': u'照片',
        'abstract': u'摘要',
        'title': u'题目',
        'text': u'正文',
        'create_time': u'创建时间',
        'update_time': u'更新时间',
        'state': u'状态',
        'category_id': u'类型ID',
        'category': u'类型',
        'tags': u'标签',
        'comments': u'评论',
        'user_id': u'作者id',
        'visit_num': u'浏览次数',
        'picture': u'配图'
    }

    @expose('/editor_pic', methods=["POST"])
    def editor_pic(self):
        image_file = request.files['editormd-image-file']
        if image_file and allowed_photo(image_file.filename):
            filename = secure_filename(image_file.filename)
            filename = str(date.today()) + '--' + filename
            print filename
            file_path = os.path.join(bpdir, 'static/editor.md/photoupdate/', filename)
            image_file.save(file_path)
            data = {
                'success': 1,
                'message': 'image of editor.md',
                'url': '/static/editor.md/photoupdate/' + filename
            }
            return json.dumps(data)
        else:
            return u"没有获得图片或图片类型不支持"

    @expose('/change_do_article', methods=["GET", "POST"])
    def change_do_article(self):
        return self.render('_change_doarticle.html')

    @expose('/create_article', methods=["GET", "POST"])
    def create_article(self):
        article_form = ArticleForm()
        article_form.picture.choices = [(picture, picture.name) for picture in
                                        Picture.query.order_by('name').filter_by(state=True)]
        article_form.tags.choices = [(tag, tag.name) for tag in Tag.query.order_by('name')]
        article_form.category.choices = [(category, category.name) for category in Category.query.order_by('name')]
        return self.render('_create_article.html', article_form=article_form)

    @expose('/save_article', methods=["GET", "POST"])
    def save_article(self):
        article_form = ArticleForm()
        article_form.tags.choices = [(tag, tag.name) for tag in Tag.query.order_by('name')]
        article_form.category.choices = [(category, category.name) for category in Category.query.order_by('name')]
        article_form.picture.choices = [(picture, picture.name) for picture
                                        in Picture.query.order_by('name').filter_by(state=True)]

        new_article = Article(title=article_form.title.data, text=article_form.text.data, html_text=article_form.html.data)
        new_article.category = article_form.category.data
        new_article.abstract = article_form.abstract.data
        new_article.tags = article_form.tags.data
        new_article.picture = article_form.picture.data

        if article_form.print_submit.data:
            new_article.state = True

        if article_form.picture.data:
            the_picture = Picture.query.filter_by(name=article_form.picture.data.name).first()
            if the_picture.name != u'暂不选择配图':
                the_picture.state = False
            db.session.add(the_picture)
        db.session.add(new_article)
        db.session.commit()

        filename = ' '.join(article_form.title.data.split())+'.md'
        with codecs.open(bpdir+'/static/blog/mdfile/'+filename, 'w',  encoding='utf-8') as f:
            f.write(article_form.text.data)

        return redirect('/huangzp/article')

    @expose('/edit_get_form/<article_id>', methods=["GET", "POST"])
    def edit_get_form(self, article_id):
        article_form = ArticleForm()
        article_form.tags.choices = [(tag, tag.name) for tag in Tag.query.order_by('name')]
        article_form.category.choices = [(category, category.name) for category in Category.query.order_by('name')]
        article_form.picture.choices = [(picture, picture.name) for picture in
                                        Picture.query.order_by('name').filter_by(state=True)]

        the_article = Article.query.filter_by(id=article_id).first()

        filename = ' '.join(the_article.title.split()) + '.md'
        try:
            os.remove(bpdir+'/static/blog/mdfile/'+filename)
        except:
            pass

        article_form.title.default = the_article.title
        article_form.text.default = the_article.text
        article_form.abstract.default = the_article.abstract
        article_form.category.default = the_article.category
        article_form.tags.default = the_article.tags
        article_form.picture.default = the_article.picture
        article_form.process()

        return self.render('_edit_article.html', article_form=article_form, article_id=article_id)

    @expose('/edit_to_save/<article_id>', methods=["GET", "POST"])
    def edit_to_save(self, article_id):
        article_form = ArticleForm()
        article_form.tags.choices = [(tag, tag.name) for tag in Tag.query.order_by('name')]
        article_form.category.choices = [(category, category.name) for category in Category.query.order_by('name')]
        article_form.picture.choices = [(picture, picture.name) for picture in
                                        Picture.query.order_by('name').filter_by(state=True)]

        the_article = Article.query.filter_by(id=article_id).first()
        the_article.title = article_form.title.data
        the_article.tags = article_form.tags.data
        the_article.category = article_form.category.data
        the_article.picture = article_form.picture.data
        the_article.text = article_form.text.data
        the_article.html_text = article_form.html.data
        the_article.abstract = article_form.abstract.data
        # else确保修改的文章状态是True然后点的保存
        if article_form.print_submit.data:
            the_article.state = True
        else:
            the_article.state = False
        #配图使用后更改状态
        if article_form.picture.data:
            the_picture = Picture.query.filter_by(name=article_form.picture.data.name).first()
            if the_picture.name != u'暂不选择配图':
                the_picture.state = False
            db.session.add(the_picture)

        db.session.add(the_article)
        db.session.commit()
        filename = ' '.join(article_form.title.data.split())+'.md'
        with codecs.open(bpdir+'/static/blog/mdfile/'+filename, 'w',  encoding='utf-8') as f:
            f.write(article_form.text.data)
        return redirect('/huangzp/article')

    @expose('/do_file',methods=["POST"])
    def do_file(self):
        md_file = request.files['file']
        if md_file and allowed_file(md_file.filename):
            fname = secure_filename(md_file.filename)
            ext = fname.rsplit('.', 1)[1]
            unix_time = int(time.time())
            new_filename = str(unix_time) + '.' + ext
            filepath = os.path.join(bpdir, 'static/blog/read_mdfile/', new_filename)
            md_file.save(filepath)
            with open(filepath, 'r') as f:
                file_context = f.read()

                # if file_context[:3] == codecs.BOM_UTF8:
                #     data = file_context[3:]
                #     print data.decode("utf-8")
                article_form = ArticleForm()

                article_form.tags.choices = [(tag, tag.name) for tag in Tag.query.order_by('name')]
                article_form.category.choices = [(category, category.name) for category in Category.query.order_by('name')]
                article_form.picture.choices = [(picture, picture.name) for picture in
                                                Picture.query.order_by('name').filter_by(state=True)]
                article_form.text.default = file_context.decode('utf-8')
                article_form.process()
                return self.render('_create_article.html', article_form=article_form)
        else:
            return u"没有获得文件或文件类型错误"

    def __init__(self, session, **kwargs):
        super(ArticleView, self).__init__(Article, session, **kwargs)


class CommentView(BaseBlogView):

    column_list = ['id', 'text', 'hidden', 'create_time', 'update_time', 'article_id', 'user_id']

    column_formatters = dict(text=macro('render_text'))

    column_searchable_list = ['text']
    column_filters = ['text', 'create_time', 'hidden']
    column_labels = {
        'id': u'序号',
        'text': u'评论',
        'hidden': u'状态',
        'create_time': u'创建时间',
        'update_time': u'更新时间',
        'article_id': u'文章id',
        'user_id': u'作者id'
    }


    def __init__(self, session, **kwargs):
        super(CommentView, self).__init__(Comment, session, **kwargs)


class TagView(BaseBlogView):

    def _list_thumbnail(view, context, model, name):
        if not model.picture or not model.picture.path:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename='blog/picture/' + 'thumb-' + model.picture.path))
    column_formatters = dict(abstract=macro('render_abstract'), picture=_list_thumbnail)

    column_list = ['id', 'photo', 'abstract', 'name', 'hidden', 'create_time', 'update_time', 'user_id', 'picture']

    column_searchable_list = ['name', 'abstract']
    column_filters = ['name', 'create_time', 'hidden']
    column_labels = {
        'id': u'序号',
        'photo': u'照片',
        'abstract': u'介绍',
        'name': u'标签',
        'hidden': u'状态',
        'create_time': u'创建时间',
        'update_time': u'更新时间',
        'user_id': u'作者id',
        'picture': u'配图缩略图'
    }

    def __init__(self, session, **kwargs):
        super(TagView, self).__init__(Tag, session, **kwargs)


class CategoryView(BaseBlogView):

    def _list_thumbnail(view, context, model, name):
        if not model.picture or not model.picture.path:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename='blog/picture/' + 'thumb-' + model.picture.path))
    column_formatters = dict(abstract=macro('render_abstract'), picture=_list_thumbnail)
    column_list = ['id', 'photo', 'abstract', 'name', 'hidden', 'create_time', 'update_time',
                   'articles', 'user_id', 'picture']

    column_searchable_list = ['name', 'abstract']
    column_filters = ['name', 'create_time', 'hidden']
    column_labels = {
        'id': u'序号',
        'photo': u'照片',
        'abstract': u'介绍',
        'name': u'类别',
        'hidden': u'状态',
        'create_time': u'创建时间',
        'update_time': u'更新时间',
        'articles': u'文章',
        'user_id': u'作者id',
        'picture': u'配图缩略图'
    }

    def __init__(self, session, **kwargs):
        super(CategoryView, self).__init__(Category, session, **kwargs)




# 钩子函数，Picture删除数据后执行
@listens_for(Picture, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(os.path.join(bpdir, 'static/blog/picture', target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(os.path.join(bpdir, 'static/blog/picture',
                                   'thumb-' + target.path))
        except OSError:
            pass


class PictureView(BaseBlogView):
    column_list = ['id', 'abstract', 'name', 'state', 'create_time', 'article', 'location', 'weather', 'user_id', 'path']

    column_labels = {
        'id': u'序号',
        'abstract': u'介绍',
        'name': u'名字',
        'state': u'状态',
        'create_time': u'创建时间',
        'article': u'文章',
        'user_id': u'作者id',
        'location': u'位置',
        'weather': u'天气',
        'path': u'缩略图'
    }

    # 覆盖path默认显示
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        print type(model.path)
        return Markup('<img src="%s">' % url_for('static',
                                                 filename='blog/picture/' + 'thumb-' + model.path))

    column_formatters = {
        'path': _list_thumbnail
    }

    # 处理上传图片名称
    def prefix_name(obj, file_data):

        parts = os.path.splitext(file_data.filename)
        return parts[0]+parts[1]
        #return secure_filename('file-%s%s' % (parts[0].encode('utf-8'), parts[1]))
    # 处理上传图片缩略图名称
    def thumb_name(filename):
        return 'thumb-'+filename

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=os.path.join(bpdir, 'static/blog/picture'),
                                      thumbnail_size=(100, 100, True),
                                      namegen=prefix_name,
                                      thumbgen=thumb_name)
    }
    def __init__(self, session, **kwargs):
        super(PictureView, self).__init__(Picture, session, **kwargs)


class MdFileView(fileadmin.FileAdmin):

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        if current_user.has_role('admin'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

    can_delete_dirs = False