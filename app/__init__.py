from flask import Flask,request,url_for
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':'wealth'}
app.config['SECRET_KEY'] = 'KeepThisS3scr3t'

db = MongoEngine(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view='login'

from app import models,views,admin,noticeboard

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if __name__ == '__main__':
	app.run()
