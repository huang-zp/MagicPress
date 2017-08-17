# -*- coding: utf-8 -*-
from MagicPress import db


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    articles = db.relationship('Article', backref='author')
    categories = db.relationship('Category', backref='author')
    tags = db.relationship('Tag', backref='author')
    comments = db.relationship('Comment', backref='author')
    location = db.Column(db.String(64))

    def __repr__(self):
        return self.name
