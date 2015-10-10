from flask import Blueprint, request, redirect, render_template, url_for,g
from flask.views import MethodView
from app.models import User
from app import app
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import login_user, logout_user, current_user, login_required
import time

@app.route('/admin',methods=['GET','POST'])
def admin_index():
    return render_template('admin/index.html')

class ListView(MethodView):
    @login_required
    def get(self):
        users = User.objects.all()
        return render_template('user/list.html',
                                users=users,
                                type=type,
                                current_user=current_user)

class DetailView(MethodView):

    form = model_form(User, exclude=['regdate'])

    def get_context(self,user_id):

        user = User.objects.get_or_404(user_id=user_id)
        form = self.form(request.form)

        context = {
                "user":user,
                "form":form
                }
        return context

    @login_required
    def get(self,user_id):
        context = self.get_context(user_id)
        return render_template('user/detail.html',**context)

users = Blueprint('admin.users',__name__,template_folder='templates')
users.add_url_rule('/admin/users/',
        view_func=ListView.as_view('list'))
users.add_url_rule('/admin/users/<user_id>/',
        view_func=DetailView.as_view('detail'))
app.register_blueprint(users)

