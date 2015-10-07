from flask import Blueprint, request, redirect, render_template, url_for,g
from flask.views import MethodView
from app.models import User,NoticeBoard
from app import app
from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import current_user, login_required

class ListView(MethodView):
    
    def get(self):
        notices = NoticeBoard.objects.all()
        return render_template('notice/list.html',
                                notices=notices,
                                current_user=current_user)

class WriteView(MethodView):
    @login_required
    def get(self):
        return render_template()


class DetailView(MethodView):

    form = model_form(User, exclude=['regdate'])

    def get_context(self,no):

        user = User.objects.get_or_404(user_id=user_id)
        form = self.form(request.form)

        context = {
                "user":user,
                "form":form
                }
        return context

    @login_required
    def get(self,no):
        context = self.get_context(user_id)
        return render_template('user/detail.html',**context)

notice = Blueprint('notice',__name__,template_folder='templates')
notice.add_url_rule('/notice/',
        view_func=ListView.as_view('list'))
notice.add_url_rule('/notice/<no>/',
        view_func=DetailView.as_view('detail'))
app.register_blueprint(notice)

