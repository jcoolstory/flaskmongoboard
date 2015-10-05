from app.models import User
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
    id = StringField('id', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
