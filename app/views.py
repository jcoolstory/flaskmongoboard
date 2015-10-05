from flask import render_template,flash, redirect,session,url_for,request,g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app,db,lm
from datetime import datetime
from app.forms import LoginForm
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    # print("login : %s" % g.user)
    # if g.user is not None and g.user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
      
      user = User.objects.get_or_404(user_id=form.id.data,
                                      password=form.password.data)
      
      login_user(user)
      return redirect(url_for('index'))

    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
  return "hello world"

@lm.user_loader
def load_user(id):
    return User.objects.get(user_id=id)