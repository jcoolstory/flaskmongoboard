from flask import Blueprint, request, redirect, render_template, url_for,g,session,abort
from flask.views import MethodView
from app.models import User,NoticeBoard,UserPrivateBoard
from app.forms import SearchForm
from .pagination import Pagination
from app import app
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import current_user, login_required
from bson.json_util import dumps
from mongoengine.queryset import Q

class ListView(MethodView):
    model = UserPrivateBoard
    pagesize =15

    def check_access(self,board):
        check = False
        if current_user.is_admin:
            check = True
        if current_user.user_id == board:
            check = True

        if not check:
            abort(404) 
        
    @login_required
    def get(self,board,page):
        self.check_access(board)

        form = SearchForm()
        
        user = User.objects.get_or_404(user_id=board)
        querys = Q(group=user)
        q = request.args.get('q',None)
        if q:
            querys =Q(title__contains=q)
        
        if page is None:
            page = 1
        start = (page-1) * self.pagesize
        
        posts = self.model.objects(querys).order_by('-no')[start:start+self.pagesize]
        count = posts.count()
        pagination = Pagination(page, self.pagesize, count)
        return render_template('private/list.html',
                                posts=posts,
                                pagination=pagination,
                                current_user=current_user,
                                form=form,
                                q=q)
                                
class DeleteView(MethodView):
    model = UserPrivateBoard
    def get(self,board,no):
        
        post = self.model.objects.get_or_404(no=no)
        post.delete()
        return redirect( url_for('private.list'))

class DetailView(MethodView):
    model = UserPrivateBoard
    def get_context(self,no):

        post = self.model.objects.get_or_404(no=no)    
        context = { "post":post }

        return context
    def get(self,board,no):
        context = self.get_context(no)
        context['post'].hitcount = context['post'].hitcount +1
        context['post'].save()
        return render_template('private/detail.html',**context)

class EditView(MethodView):

    model = UserPrivateBoard
    form = None
    
    def get_context(self,no):
        print(no)
        if no :
            post = self.model.objects.get_or_404(no=no)
            form = self.form(obj=post)
            create = False
            if request.method == 'POST':
                form = self.form(request.form, inital=post._data)
            else:

                form = self.form(obj=post)
        else:
            post = self.model()
            create = True
            form = self.form(request.form)#model_form(NoticeBoard)

        context = { "post":post,
                    "form":form,
                    "create":create }
        return context

    @login_required
    def get(self,board,no):
         
        self.form = model_form(self.model, exclude=['user_id','regdate','group','manager_id'])
        context = self.get_context(no)        
        return render_template('private/edit.html',**context)

    @login_required
    def post(self,board,no):
        self.form = model_form(self.model, exclude=['user_id','regdate','group','manager_id'])
        context = self.get_context(no)
        form = context.get('form')
        if form.validate():
            current=User.objects.get(user_id=current_user.user_id)
            print("board:",board)
            user = User.objects.get_or_404(user_id=board)
            post = self.model(user_id=current,
                                manager_id=current,group=user,
                                title=form.title.data,
                                body=form.body.data )
            post.save()
            return redirect( url_for('private.list',board=board))
        else:
            print(form.errors)

        return render_template('private/edit.html',**context)

notice = Blueprint('private',__name__,template_folder='templates')
notice_func = ListView.as_view('list')
notice.add_url_rule('/private/<board>', defaults={'page':1},view_func=notice_func)
notice.add_url_rule('/private/<board>/<int:page>', view_func=notice_func)
notice.add_url_rule('/private/<board>/detail/<no>/', view_func=DetailView.as_view('detail'))
notice.add_url_rule('/private/<board>/edit/<no>/', view_func=EditView.as_view('edit'))
notice.add_url_rule('/private/<board>/create', defaults={'no':None},
                                       view_func=EditView.as_view('create'))
app.register_blueprint(notice)
