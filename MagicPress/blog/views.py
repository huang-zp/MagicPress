# coding:utf-8
import json
import os
from flask import redirect

from flask import render_template, request
from config import bpdir

from MagicPress.blog import blog
from .models import Article, Category
from MagicPress import db


# @blog.route('/file', methods=["POST"])
# def file():
#     imagefile = request.files['editormd-image-file']
#     filepath = os.path.join(bpdir, 'static/editor.md/photoupdate/', imagefile.filename)
#     imagefile.save(filepath)
#     data = {
#         'success': 1,
#         'message': 'image of editor.md',
#         'url': 'static/editor.md/photoupdate/' + imagefile.filename
#     }
#     return json.dumps(data)


@blog.route('/', methods=["GET", "POST"])
def index():

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).filter_by(state=True).paginate(
        page, per_page=3, error_out=False
    )
    articles = pagination.items
    return render_template('blog/index.html', articles=articles, pagination=pagination)


@blog.route('/article/<int:article_id>', methods=["GET", "POST"])
def article(article_id):

    article = Article.query.filter_by(id=article_id).first()
    next_article = db.session.query(Article).filter(Article.id < article_id).order_by(Article.id.desc()).first()
    pre_article = db.session.query(Article).filter(Article.id > article_id).order_by(Article.id.asc()).first()
    return render_template('blog/article.html', article=article, next_article=next_article, pre_article=pre_article)


@blog.route('/category', defaults={'id': None})
@blog.route('/category/<id>', methods=["GET", "POST"])
def category(id):
    if not id:
        categories = Category.query.all()
        return render_template('blog/categories.html', categories=categories)
    else:
        articles = Category.query.filter_by(id=id).first().articles
        return render_template('blog/category.html', articles=articles)
