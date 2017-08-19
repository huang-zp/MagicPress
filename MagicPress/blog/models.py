# -*- coding: utf-8 -*-
from datetime import datetime
from MagicPress import db
from random import Random
from datetime import date

def random_str(randomlength=5):
    _str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        _str += chars[random.randint(0, length)]
    return str(date.today()) + '-' + _str + '-'

articles_tags = db.Table('articles_tags',
                      db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default=random_str)
    abstract = db.Column(db.Text())
    location = db.Column(db.String(64))
    create_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weather = db.Column(db.String(64))
    path = db.Column(db.String(128))
    state = db.Column(db.Boolean, default=True)
    articles = db.relationship('Article', backref='picture')
    tags = db.relationship('Tag', backref='picture')
    categories = db.relationship('Category', backref='picture')


    def __repr__(self):
        return self.name



class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer, db.ForeignKey('pictures.id'))
    abstract = db.Column(db.Text())
    title = db.Column(db.String(64), index=True)
    text = db.Column(db.Text())
    html_text = db.Column(db.Text())
    create_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    state = db.Column(db.Boolean, default=False)
    visit_num = db.Column(db.Integer, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    tags = db.relationship('Tag', secondary=articles_tags, backref=db.backref('articles', lazy='dynamic'))
    comments = db.relationship('Comment', backref='article')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.title


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer, db.ForeignKey('pictures.id'))
    abstract = db.Column(db.Text())
    name = db.Column(db.String(64), unique=True, index=True)
    hidden = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    articles = db.relationship('Article', backref='category')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.name


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer, db.ForeignKey('pictures.id'))
    abstract = db.Column(db.Text())
    name = db.Column(db.String(64), unique=True, index=True)
    hidden = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.name


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    hidden = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    def __repr__(self):
        return self.text

