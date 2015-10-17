from flask import Blueprint, request, redirect, render_template, url_for,g
from flask.views import MethodView
from app.models import User,UserGrade
from app.forms import SearchForm,ExtraForm,UserDetailForm
from app import app
from .pagination import Pagination
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import login_user, logout_user, current_user, login_required
from mongoengine.queryset import Q
import time,logging,sys

@app.route('/admin',methods=['GET','POST'])
def admin_index():
    return render_template('admin/index.html')

class ListView(MethodView):
    pagesize =15
    @login_required    
    def get(self):
        if not current_user.is_admin:
            return redirect( url_for('index'))
        querys = Q()
        form = SearchForm()
        
        page = int(request.args.get('page',1))        
        p = request.args.get('q',None)
        if p:
            querys = Q(user_id__contains=p)
        start = (page-1) * self.pagesize
        users = User.objects(querys)[start:start+self.pagesize]
        count = users.count()
        pagination = Pagination(page, self.pagesize, count)

        return render_template('user/list.html',
                                users=users,p=p,form=form,
                                pagination=pagination,
                                current_user=current_user,)

class DetailView(MethodView):
    #form =UserDetailForm
    
    form = model_form(User, exclude=['user_id','regdate','password','extra'],field_args={'grade':{'label_attr':'name'}})

    def get_context(self,user_id):
        user = User.objects.get_or_404(user_id=user_id)
        
        if request.method == 'POST':
            form = self.form(request.form, inital=user._data)
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
        logging.info(request.form)
        if form.validate():
            user =context.get('user')
            form.populate_obj(user)            
            user.extra.data = request.form['extra_data']
            user.save()
            return redirect( url_for('admin.users.detail',user_id=user_id))
        else:
            logging.info(form.errors)
        return render_template('user/detail.html',**context)

users = Blueprint('admin.users',__name__,template_folder='templates')
users.add_url_rule('/admin/users/', view_func=ListView.as_view('list'))
users.add_url_rule('/admin/users/<user_id>/', view_func=DetailView.as_view('detail'))
app.register_blueprint(users)

