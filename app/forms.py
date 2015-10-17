from app.models import User
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField,PasswordField,SelectField,RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
    id = EmailField('id', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterPersonForm(Form):
    user_id = EmailField('user_id', validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])

class SearchForm(Form):
    q = StringField('q')

class ExtraForm(Form):
    data = StringField('data')

class UserDetailForm(Form):
    name = StringField('name',validators=[DataRequired()])
    grade =SelectField('grade',choices=[("1","2")]) 
    extra_data = TextAreaField('extra-data')