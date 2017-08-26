# coding:utf-8
import json
import os
from flask import redirect, url_for, flash
from flask import render_template, request
from config import bpdir
from datetime import datetime
from MagicPress.blog import blog
from .models import Article, Category, Comment
from .forms import CommentForm
from MagicPress import db, cache
from flask_security import login_required
from flask import current_app
from MagicPress.utils.cache import cached, key_prefix
from MagicPress.utils.ip import get_ip_info
from MagicPress.utils.filter import gfw
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


@cache.cached(key_prefix='get_theme')
def get_theme():
    with open(bpdir+'/static/theme', 'r') as f:
       theme = f.read()
    return theme


@blog.route('/change_theme/<string:theme>')
@login_required
def change_theme(theme):
    cache.clear()
    with open(bpdir+'/static/theme', 'w') as f:
        f.write(theme)
    return redirect('/')


@blog.route('/', methods=["GET", "POST"])
# @cached(timeout=5 * 60, key='blog_view_%s')
@cache.cached(timeout=300, key_prefix=key_prefix, unless=None)
def index():

    print get_theme()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).filter_by(state=True).paginate(
        page, per_page=3, error_out=False
    )
    articles = pagination.items
    categories = Category.query.all()
    return render_template(get_theme() + '/index.html', articles=articles, pagination=pagination,
                           categories=categories)


@blog.route('/article/<int:article_id>', methods=["GET", "POST"])
@cached()
def article(article_id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(username=comment_form.name.data)
        new_comment.text = comment_form.text.data
        new_comment.create_time = datetime.utcnow()
        new_comment.site = comment_form.site.data
        new_comment.email = comment_form.email.data
        new_comment.ip = request.remote_addr
        new_comment.language = request.accept_languages.best
        new_comment.os = request.user_agent.platform
        new_comment.browser = request.user_agent.browser
        new_comment.article_id = str(request.base_url).split('/')[-1]
        info = get_ip_info(request.remote_addr)
        new_comment.location = info['country']+info['region']+info['city']
        new_comment.network = info['isp']
        if gfw.filter(comment_form.text.data) or gfw.filter(comment_form.name.data):
            new_comment.hidden = False
            flash(u'评论失败、含有敏感字符！')
        else:
            new_comment.hidden = True
        db.session.add(new_comment)
        db.session.commit()
    the_article = Article.query.filter_by(id=article_id).first()
    next_article = db.session.query(Article).filter(Article.id < article_id).order_by(Article.id.desc()).first()
    pre_article = db.session.query(Article).filter(Article.id > article_id).order_by(Article.id.asc()).first()
    comments = Comment.query.filter_by(article_id=article_id, hidden=True).all()
    return render_template(get_theme() + '/article.html', article=the_article, next_article=next_article,
                           pre_article=pre_article, comment_form=comment_form, comments=comments)


@blog.route('/category', defaults={'article_id': None})
@blog.route('/category/<int:article_id>', methods=["GET", "POST"])
@cache.cached(timeout=300, key_prefix='blog_view_%s', unless=None)
def category(article_id):
    if not article_id:
        categories = Category.query.all()
        return render_template(get_theme() + '/categories.html', categories=categories)
    else:
        articles = Category.query.filter_by(id=article_id).first().articles
        return render_template(get_theme() + '/category.html', articles=articles)


@blog.route('/archive', methods=["GET", "POST"])
@cache.cached(timeout=300, key_prefix='blog_view_%s', unless=None)
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
    return render_template(get_theme() + '/archive.html', time_list=time_list, article_list=article_list)


@blog.route('/comment/<int:article_id>', methods=['GET', 'POST'])
def comment(article_id):
    comment_form = CommentForm(request.form)
    cache_key = 'view_%s' % url_for('blog.article', article_id=article_id)
    cache.delete(cache_key)
    cache.clear()
    if comment_form.validate_on_submit():
        pass
    return redirect(url_for('blog.article', article_id=article_id))
