from flask import Blueprint, request, redirect, render_template, url_for,g,session
from flask.views import MethodView
from app.models import User,NoticeBoard
from .pagination import Pagination
from app import app
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import current_user, login_required
from bson.json_util import dumps

board_map = {'notice':NoticeBoard}

class ListView(MethodView):

    pagesize =15
    def get(self,board,page):
        
        post_obj = board_map[board]
        if page is None:
            page = 1
        start = (page-1) * self.pagesize
        
        count = post_obj.objects.all().count()
        notices = post_obj.objects.all().order_by('-no')[start:start+self.pagesize]
        pagination = Pagination(page, self.pagesize, count)
        return render_template('notice/list.html',
                                notices=notices,
                                pagination=pagination,
                                current_user=current_user)
class DeleteView(MethodView):
    def get(self,board,no):
        post_obj = board_map[board]
        post = post_obj.objects.get_or_404(no=no)
        post.delete()
        return redirect( url_for('notice.list'))

class DetailView(MethodView):

    def get_context(self,post_obj,no):

        post = post_obj.objects.get_or_404(no=no)    
        context = { "post":post }

        return context
    def get(self,board,no):
        post_obj = board_map[board]
        context = self.get_context(post_obj,no)
        context['post'].hitcount = context['post'].hitcount +1
        context['post'].save()
        return render_template('notice/detail.html',**context)

class EditView(MethodView):

    form = None
    
    def get_context(self,post_obj,no):
        print(no)
        if no :
            post = post_obj.objects.get_or_404(no=no)
            form = self.form(obj=post)
            create = False
        else:
            post = post_obj()
            create = True
            form = self.form(request.form)#model_form(NoticeBoard)

        context = { "post":post,
                    "form":form,
                    "create":create }
        return context

    @login_required
    def get(self,board,no):
        post_obj = board_map[board]
        self.form = model_form(post_obj, exclude=['user_id','regdate'])
        context = self.get_context(post_obj,no)        
        return render_template('notice/edit.html',**context)

    @login_required
    def post(self,board,no):
        post_obj = board_map[board]
        self.form = model_form(post_obj, exclude=['user_id','regdate'])
        context = self.get_context(post_obj,no)
        form = context.get('form')
        if form.validate():
            current=User.objects.get(user_id=current_user.user_id)
            post = post_obj(user_id=current,
                title=form.title.data,
                body=form.body.data )
            post.save()
            return redirect( url_for('notice.list'))
        return render_template('notice/edit.html',**context)

notice = Blueprint('notice',__name__,template_folder='templates')
notice_func = ListView.as_view('list')
notice.add_url_rule('/bbs/<board>', defaults={'page':1},view_func=notice_func)
notice.add_url_rule('/bbs/<board>/<int:page>', view_func=notice_func)
notice.add_url_rule('/bbs/<board>/detail/<no>/', view_func=DetailView.as_view('detail'))
notice.add_url_rule('/bbs/<board>/edit/<no>/', view_func=EditView.as_view('edit'))
notice.add_url_rule('/bbs/<board>/create', defaults={'no':None},
                                       view_func=EditView.as_view('create'))
# notice.add_url_rule('/notice', defaults={'page':1},view_func=notice_func)
# notice.add_url_rule('/notice/', defaults={'page':1},view_func=notice_func)
# notice.add_url_rule('/notice/<int:page>', view_func=notice_func)

# notice.add_url_rule('/notice/detail/<no>/', view_func=DetailView.as_view('detail'))
# notice.add_url_rule('/notice/edit/<no>/', view_func=EditView.as_view('edit'))
# notice.add_url_rule('/notice/create', defaults={'no':None},
#                                       view_func=EditView.as_view('create'))
# notice.add_url_rule('/notice/delete/<no>/',view_func=DeleteView.as_view('delete'))
app.register_blueprint(notice)
