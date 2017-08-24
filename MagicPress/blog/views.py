# coding:utf-8
import json
import os
from flask import redirect, url_for

from flask import render_template, request
from config import bpdir

from MagicPress.blog import blog
from .models import Article, Category
from MagicPress import db
from flask_security import login_required
from flask import current_app

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


@blog.route('/change_theme/<string:theme>')
@login_required
def change_theme(theme):
    current_app.config['THEME'] = theme
    return redirect('/')



@blog.route('/', methods=["GET", "POST"])
def index():

    print current_app.config['THEME']
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).filter_by(state=True).paginate(
        page, per_page=3, error_out=False
    )
    articles = pagination.items
    categories = Category.query.all()
    return render_template(current_app.config['THEME'] + '/index.html', articles=articles, pagination=pagination,
                           categories=categories)


@blog.route('/article/<int:article_id>', methods=["GET", "POST"])
def article(article_id):
    a = request
    the_article = Article.query.filter_by(id=article_id).first()
    next_article = db.session.query(Article).filter(Article.id < article_id).order_by(Article.id.desc()).first()
    pre_article = db.session.query(Article).filter(Article.id > article_id).order_by(Article.id.asc()).first()
    return render_template(current_app.config['THEME'] + '/article.html', article=the_article, next_article=next_article, pre_article=pre_article)


@blog.route('/category', defaults={'id': None})
@blog.route('/category/<id>', methods=["GET", "POST"])
def category(id):
    if not id:
        categories = Category.query.all()
        return render_template(current_app.config['THEME'] + '/categories.html', categories=categories)
    else:
        articles = Category.query.filter_by(id=id).first().articles
        return render_template(current_app.config['THEME'] + '/category.html', articles=articles)


@blog.route('/archive', methods=["GET", "POST"])
def archive():
    all_articles = Article.query.order_by(Article.create_time.desc()).all()
    time_list = {}
    article_list = [[]]
    flag = 0
    time_list[flag] = str(all_articles[0].create_time).split('-', 2)[:2]
    for the_article in all_articles:

        year_month = str(the_article.create_time).split('-', 2)[:2]
        if year_month in time_list.values():
            article_list[flag].append(the_article)
        else:
            flag += 1
            time_list[flag] = year_month
            article_list.append([])
            article_list[flag].append(the_article)
    print time_list
    return render_template(current_app.config['THEME'] + '/archive.html', time_list=time_list, article_list=article_list)





