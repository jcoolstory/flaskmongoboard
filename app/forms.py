from app.models import User
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
    id = StringField('id', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class RegisterPersonForm(Form):
    user_id = StringField('user_id', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    password2 = StringField('password2', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    