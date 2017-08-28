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
from random import Random
from datetime import datetime
from MagicPress.utils.qiniuapi import get_link
from MagicPress.utils.tinifyapi import ting_pic

def random_str(randomlength=5):
    _str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        _str += chars[random.randint(0, length)]
    return _str


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

    column_list = ['id', 'title', 'abstract', 'text', 'create_time', 'update_time', 'state',
                   'visit_num', 'category', 'tags', 'comments', 'user', 'picture']

    column_searchable_list = ['title']
    column_filters = ['title', 'create_time', 'state']

    column_editable_list = ['state', 'visit_num', 'tags', 'category']

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
        'title': u'题目',
        'abstract': u'摘要',
        'text': u'正文',
        'create_time': u'创建时间',
        'update_time': u'更新时间',
        'state': u'状态',
        'category': u'类型',
        'tags': u'标签',
        'comments': u'评论',
        'user': u'作者',
        'visit_num': u'浏览次数',
        'picture': u'配图'
    }

    @expose('/editor_pic', methods=["POST"])
    def editor_pic(self):
        image_file = request.files['editormd-image-file']
        if image_file and allowed_photo(image_file.filename):
            filename = secure_filename(image_file.filename)
            filename = str(date.today()) + '-' + random_str() + '-' + filename
            print filename
            file_path = os.path.join(bpdir, 'static/editor.md/photoupdate/', filename)
            qiniu_path = os.path.join(bpdir, 'static/blog/qiniu_pic/', filename)
            image_file.save(file_path)
            ting_pic(file_path, qiniu_path)
            qiniu_link = get_link(qiniu_path, filename)
            data = {
                'success': 1,
                'message': 'image of editor.md',
                'url': qiniu_link
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
        article_form.create_time.default = datetime.utcnow()
        article_form.update_time.default = datetime.utcnow()
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
        new_article.create_time = article_form.create_time.data
        new_article.update_time = article_form.update_time.data

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
        if not article_form.print_submit.data:
            return redirect(url_for('.edit_get_form', article_id=new_article.id))
        return redirect('/huangzp/article')

    @expose('/edit_get_form/<article_id>', methods=["GET", "POST"])
    def edit_get_form(self, article_id):
        article_form = ArticleForm()
        article_form.tags.choices = [(tag, tag.name) for tag in Tag.query.order_by('name')]
        article_form.category.choices = [(category, category.name) for category in Category.query.order_by('name')]
        article_form.picture.choices = [(picture, picture.name) for picture in
                                        Picture.query.order_by('name').filter_by(state=True)]

        the_article = Article.query.filter_by(id=article_id).first()

        # 修改文章默认配图
        if the_article.picture and the_article.picture.name != u'暂不选择配图':
            article_form.picture.choices.append((the_article.picture, the_article.picture.name))


        article_form.title.default = the_article.title
        article_form.text.default = the_article.text
        article_form.abstract.default = the_article.abstract
        article_form.category.default = the_article.category
        article_form.tags.default = the_article.tags
        article_form.picture.default = the_article.picture
        article_form.create_time.default = the_article.create_time
        article_form.update_time.default = the_article.update_time
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

        # 删除旧备份
        old_filename = ' '.join(the_article.title.split()) + '.md'
        try:
            os.remove(bpdir+'/static/blog/mdfile/'+old_filename)
        except:
            pass

        # 有时候直接删除已经关联文章的照片，会造成文章的照片属性为空
        if not the_article.picture:
            new_picture = Picture.query.filter_by(name=article_form.picture.data.name).first()
            if new_picture.name != u'暂不选择配图':
                new_picture.state = False
            db.session.add(new_picture)
        else:
            new_picture = Picture.query.filter_by(name=article_form.picture.data.name).first()
            old_picture = Picture.query.filter_by(name=the_article.picture.name).first()
            if new_picture == old_picture:
                pass
            elif new_picture.name == u'暂不选择配图':
                new_picture.state = True
                old_picture.state = True
                db.session.add(new_picture, old_picture)
            else:
                new_picture.state = False
                old_picture.state = True
                db.session.add(new_picture, old_picture)

        the_article.title = article_form.title.data
        the_article.tags = article_form.tags.data
        the_article.category = article_form.category.data
        the_article.picture = article_form.picture.data
        the_article.text = article_form.text.data
        the_article.html_text = article_form.html.data
        the_article.abstract = article_form.abstract.data
        the_article.create_time = article_form.create_time.data
        the_article.update_time = article_form.update_time.data
        # else确保修改的文章状态是True然后点的保存
        if article_form.print_submit.data:
            the_article.state = True
        else:
            the_article.state = False


        db.session.add(the_article)
        db.session.commit()
        new_filename = ' '.join(article_form.title.data.split())+'.md'
        with codecs.open(bpdir+'/static/blog/mdfile/'+new_filename, 'w',  encoding='utf-8') as f:
            f.write(article_form.text.data)
        if not article_form.print_submit.data:
            return redirect(url_for('.edit_get_form', article_id=the_article.id))
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

    column_list = ['id', 'text', 'hidden', 'create_time', 'article', 'username', 'email', 'site', 'ip', 'location', 'os'
                   , 'browser', 'language', 'network']

    column_editable_list = ['hidden']

    column_searchable_list = ['text']
    column_filters = ['text', 'create_time', 'hidden']
    column_labels = {
        'id': u'序号',
        'text': u'评论',
        'hidden': u'状态',
        'create_time': u'创建时间',
        'article': u'文章',
        'username': u'姓名',
        'email': u'邮箱',
        'site': u'站点',
        'ip': u'Ip',
        'location': u'IP地点',
        'os': u'平台',
        'browser': u'浏览器',
        'language': u'语言',
        'network': u'网络接入商'
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

    column_editable_list = ['hidden']

    column_list = ['id', 'name', 'abstract', 'hidden', 'create_time', 'update_time', 'user', 'picture']

    column_searchable_list = ['name', 'abstract']
    column_filters = ['name', 'create_time', 'hidden']
    column_labels = {
        'id': u'序号',
        'name': u'标签',
        'abstract': u'介绍',
        'hidden': u'状态',
        'create_time': u'创建时间',
        'update_time': u'更新时间',
        'user': u'作者',
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
    column_list = ['id', 'name', 'abstract', 'hidden', 'create_time', 'update_time',
                   'articles', 'user', 'picture']

    column_editable_list = ['hidden']
    column_searchable_list = ['name', 'abstract']
    column_filters = ['name', 'create_time', 'hidden']
    column_labels = {
        'id': u'序号',
        'name': u'类别',
        'abstract': u'介绍',
        'hidden': u'状态',
        'create_time': u'创建时间',
        'update_time': u'更新时间',
        'articles': u'文章',
        'user': u'作者',
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
    column_list = ['id', 'name', 'state', 'abstract', 'create_time', 'articles', 'location', 'weather', 'user', 'path']
    column_editable_list = ['state', 'location', 'weather']
    column_labels = {
        'id': u'序号',
        'name': u'名字',
        'state': u'状态',
        'abstract': u'介绍',
        'create_time': u'创建时间',
        'articles': u'所关联文章',
        'user': u'作者',
        'location': u'位置',
        'weather': u'天气',
        'path': u'缩略图'
    }

    # 覆盖path默认显示
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        return Markup('<img src="%s">' % url_for('static',
                                                 filename='blog/picture/' + 'thumb-' + model.path))

    column_formatters = {
        'path': _list_thumbnail
    }

    # 处理上传图片名称
    def prefix_name(obj, file_data):

        parts = os.path.splitext(file_data.filename)
        return str(date.today()) + '-' + random_str() + '-' + parts[0]+parts[1]
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
                                      max_size=(720, 480, True),
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