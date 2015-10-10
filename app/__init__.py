from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':'3wm'}
app.config['SECRET_KEY'] = 'KeepThisS3scr3t'

db = MongoEngine(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view='login'

from app import models,views,admin,noticeboard

if __name__ == '__main__':
	app.run()
