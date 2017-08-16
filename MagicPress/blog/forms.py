# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, StringField, SelectField, DateTimeField, SelectMultipleField
from wtforms.validators import DataRequired
from .models import Tag, Category, Picture


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

class ArticleForm(Form):
    title = StringField(u"文章标题", validators=[DataRequired()])
    text = TextAreaField(u"文章内容", validators=[DataRequired()])
    picture = SelectField(u'配图', coerce=_string_to_picture)
    html = TextAreaField("html_text")
    tags = SelectMultipleField(u'标签', coerce=_string_to_tag)
    abstract = TextAreaField(u"文章摘要")
    category = SelectField(u'类别', coerce=_string_to_category)
    print_submit = SubmitField(u"保存")
    save_submit = SubmitField(u"发布")



