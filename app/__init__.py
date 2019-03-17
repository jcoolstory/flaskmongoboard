from flask import Flask,request,url_for
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
import hashlib,sys,logging


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)

# mongodb set
app.config["MONGODB_SETTINGS"] = {'DB':'wealth'}
app.config['SECRET_KEY'] = '2ad830a92da34be4981928f285888080'

db = MongoEngine(app)

# login manager set
lm = LoginManager()
lm.init_app(app)
lm.login_view='login'

def gen_hash(string):
    return hashlib.sha256(bytearray(string,encoding='utf8')).hexdigest()

from app import models,views,admin, noticeboard,privateboardView

def url_for_other_page(page):
    args = dict(request.view_args, **request.args)
    args['page'] = page
    return url_for(request.endpoint, **args)

def url_for_bbs():
    return request.view_args['board']

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['url_for_bbs'] = url_for_bbs


if __name__ == '__main__':
	app.run()
