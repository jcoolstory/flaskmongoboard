from flask import render_template,flash, redirect,session,url_for,request,g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app,db,lm,gen_hash
from datetime import datetime
from app.forms import LoginForm,RegisterPersonForm
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
      user = User.objects.get_or_404(user_id=form.id.data,
                                     password=gen_hash(form.password.data))
      
      login_user(user)
      session['user_obj'] = user
      return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html',
                           title='Sign In',
                           form=form,)

@app.route('/register',methods=['GET','POST'])
def register():
  form = RegisterPersonForm()
  print("form.validate_on_submit():",form.validate_on_submit())
  if form.validate_on_submit():
    if not form.password.data == form.password2.data:
      return redirect(url_for('register'))

    user = User(user_id=form.user_id.data,
                name=form.name.data,
                password=form.password.data)
    user.set_password(form.password.data)
    user.save()

    return redirect(url_for('index'))
  else:
    return render_template('register.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@lm.user_loader
def load_user(id):
    return User.objects.get(user_id=id)
