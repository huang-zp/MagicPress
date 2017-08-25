# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField, DateTimeField, SelectMultipleField, TextField
from wtforms.validators import DataRequired, Email
from .models import Tag, Category, Picture

# Select fields keep a choices property which is a sequence of (value, label) pairs.
# The value portion can be any type in theory, but as form data is sent by the browser as strings,
# you will need to provide a function which can coerce the string representation back to a comparable object.

def _string_to_tag(string):
    if isinstance(string, unicode):
        return Tag.query.filter_by(name=string).first()
    else:
        return string

def _string_to_category(string):
    if isinstance(string, unicode):
        return Category.query.filter_by(name=string).first()
    else:
        return string

def _string_to_picture(string):
    if isinstance(string, unicode):
        return Picture.query.filter_by(name=string).first()
    else:
        return string

class ArticleForm(FlaskForm):
    title = StringField(u"文章标题", validators=[DataRequired()])
    text = TextAreaField(u"文章内容", validators=[DataRequired()])
    picture = SelectField(u'配图', coerce=_string_to_picture)
    html = TextAreaField("html_text")
    tags = SelectMultipleField(u'标签', coerce=_string_to_tag)
    create_time = DateTimeField(u'创建时间')
    update_time = DateTimeField(u'更新时间')
    abstract = TextAreaField(u"文章摘要")
    category = SelectField(u'类别', coerce=_string_to_category)
    print_submit = SubmitField(u"保存")
    save_submit = SubmitField(u"发布")


class CommentForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    name = StringField(u'Name', validators=[DataRequired()])
    email = StringField(u'Email', validators=[Email(), DataRequired()])
    site = StringField(u'Site')
    comment = SubmitField(u'Comment')



