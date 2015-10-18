from app.models import User,NoticeBoard,UserExtra,UserGrade
from app import gen_hash
import random
User.objects.delete()
NoticeBoard.objects.delete()
UserGrade.objects.delete()
idtoken = ['test','kim']
with open('names.txt','r') as f:
    txt = f.read()
idtoken = txt.splitlines()

gradelist = {'user':1,'manager':100,'admin':1000}

for gname,gnumber in gradelist.items():
    grade= UserGrade(name=gname,grade=gnumber)
    grade.save()
grades = list(UserGrade.objects.all())
for token in idtoken:
    user = User(user_id='%s@test.com'%token,
                name=token,extra =UserExtra(),
                password=gen_hash(token),
                grade=random.choice(grades))
    user.save()

users = User.objects
with open('title.txt','r',encoding='utf8') as f:
    txt = f.read()
titles = [x for x in txt.splitlines() if not x =='' ]
with open('content.html','r',encoding='utf8') as f:
    content = f.read()
for index in range(50):
    user_id = random.choice(users)
    title = random.choice(titles)
    body = content
    hitcount = random.choice(range(10000))
    post = NoticeBoard(user_id=user_id,
                        title=title,
                        body = body,
                        hitcount = hitcount
        )

    post.save()
