from app.models import User,NoticeBoard
from app import gen_hash
import random
User.objects.delete()
NoticeBoard.objects.delete()
idtoken = ['test','kim']
with open('names.txt','r') as f:
    txt = f.read()
idtoken = txt.splitlines()

for token in idtoken:
    user = User(user_id='%s@test.com'%token,
                name=token,
                password=gen_hash(token))
    user.save()

users = User.objects
with open('title.txt','r',encoding='utf8') as f:
    txt = f.read()
titles = [x for x in txt.splitlines() if not x =='' ]
with open('content.html','r',encoding='utf8') as f:
    content = f.read()
for index in range(5000):
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