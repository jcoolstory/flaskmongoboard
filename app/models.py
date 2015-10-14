import datetime
from app import db
from flask import url_for

class UserExtra(db.EmbeddedDocument):
	data = db.StringField()

class User(db.Document):
    user_id = db.EmailField(max_length=40, required=True, unique=True)
    name = db.StringField(max_length=100,required=True)
    password = db.StringField(max_length=40, required=True)
    regdate = db.DateTimeField(default=datetime.datetime.now, required=True)
    grade = db.StringField(max_length=100,default='user')

    financial = db.ReferenceField('UserFinancial')

    @property
    def is_admin(self):
        print (self.grade)
        return self.user_id == "admin@test.com" or self.grade =="admin"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % (self.user_id)
    
    def get_id(self):
        try:
            return unicode(self.user_id)  # python 2
        except NameError:
            return str(self.user_id)  # python 3

class UserFinancial(db.Document):
	memo = db.StringField()	

class NoticeBoard(db.Document):
    no = db.SequenceField(required=True, unique=True)
    user_id = db.ReferenceField('User',required=True)
    title = db.StringField(max_length=200, required=True)
    body =  db.StringField(required=True)
    regdate =db.DateTimeField(default=datetime.datetime.now, required=True)
    hitcount = db.IntField(default=0)

class BoardList(db.Document):
    title = db.StringField(max_length='100')
