from flask import Blueprint, request, redirect, render_template, url_for,g
from flask.views import MethodView
from app.models import User
from app import app
from .pagination import Pagination
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import login_user, logout_user, current_user, login_required
import time

@app.route('/admin',methods=['GET','POST'])
def admin_index():
    return render_template('admin/index.html')

class ListView(MethodView):
    pagesize =15
    @login_required
    
    def get(self):
        if not current_user.is_admin:
            return redirect( url_for('index'))
        # if page is None:
        # page = 1
        page = int(request.args.get('page',1))
        count = User.objects.all().count()
        start = (page-1) * self.pagesize
        users = User.objects.all()[start:start+self.pagesize]
        pagination = Pagination(page, self.pagesize, count)
        return render_template('user/list.html',
                                users=users,
                                type=type,
                                pagination=pagination,
                                current_user=current_user)

class DetailView(MethodView):

    form = model_form(User, exclude=['user_id','regdate','extra'])

    def get_context(self,user_id):

        user = User.objects.get_or_404(user_id=user_id)
        
        if request.method == 'POST':
            form = self.form(request.form, inital=user._data)
            print ([x.label for x in form])
            print(form.name)
            print(form.password)
        else:
            form = self.form(obj=user)
        context = { "user":user,
                    "form":form }
        return context

    @login_required
    def get(self,user_id):
        if not current_user.is_admin:
            return redirect( url_for('index'))
        context = self.get_context(user_id)
        return render_template('user/detail.html',**context)

    @login_required
    def post(self,user_id):
        if not current_user.is_admin:
            return redirect( url_for('index'))
        context = self.get_context(user_id)
        form = context.get('form')
        print ('form.validate', form.validate())
        if form.validate():
            user =context.get('user')
            # user = User(user_id=current,
            #     title=form.title.data,
            #     body=form.body.data )
            form.populate_obj(user)            
            user.save()
            return redirect( url_for('admin.users.detail',user_id=user_id))
        return render_template('user/detail.html',**context)

users = Blueprint('admin.users',__name__,template_folder='templates')
users.add_url_rule('/admin/users/',
        view_func=ListView.as_view('list'))
users.add_url_rule('/admin/users/<user_id>/',
        view_func=DetailView.as_view('detail'))
app.register_blueprint(users)

