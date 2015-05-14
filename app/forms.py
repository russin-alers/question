from flask import g
from flask.ext.login import current_user
from wtforms import StringField, PasswordField, validators, TextAreaField
from flask.ext.wtf import Form
from app import app


class AddQuestionForm(Form):
    question = StringField('Question', validators=[validators.length(3, 30)])
    details = TextAreaField('Description', validators=[validators.optional()])


class LoginForm(Form):
    name = StringField('Login', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])


class AnswerForm(Form):
    answer = TextAreaField('Answer', validators=[validators.length(3)])


@app.before_request
def before_request():
    g.user = current_user
