# coding:utf-8
import json
import os
from flask import redirect

from flask import render_template, request
from config import bpdir

from MagicPress.blog import blog
from .models import Article


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
    articles = Article.query.filter_by(state=True).all()
    return render_template('blog/index.html', articles=articles)

@blog.route('/article/<int:id>', methods=["GET", "POST"])
def article(id):
    article = Article.query.filter_by(id=id).first()
    return render_template('blog/article.html', article=article)
