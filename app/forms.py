from app.models import User
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
    id = EmailField('id', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class RegisterPersonForm(Form):
    user_id = EmailField('user_id', validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    password2 = StringField('password2', validators=[DataRequired()])