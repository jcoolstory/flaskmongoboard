import datetime
from app import db,gen_hash
from flask import url_for

class UserExtra(db.EmbeddedDocument):
    data = db.StringField()
    follower = db.ListField(db.ReferenceField('User'))

class UserGrade(db.Document):
    name = db.StringField(default="user")

    def __str__(self):
        return self.name

class User(db.Document):
    user_id = db.EmailField(max_length=100, required=True, unique=True)
    name = db.StringField(max_length=100,required=True)
    password = db.StringField(max_length=64, required=True)
    regdate = db.DateTimeField(default=datetime.datetime.now, required=True)
    grade = db.ReferenceField('UserGrade')
    extra = db.EmbeddedDocumentField('UserExtra',default=None)
    financial = db.ReferenceField('UserFinancial')

    def set_password(self,password):
        self.password = gen_hash(password)

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

    def __str__(self):
        return self.name

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
