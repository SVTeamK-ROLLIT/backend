#from __future__ import absolute_import,unicode_literals #이건 뭔데 둘 다 있지?
from backend.celery import app #앱을 가져와야 하나봐
from .cartoon import cartoonizer,email
#비동기 작업 실시 
@app.task
def cartoon_task(request): 
    r = cartoonizer(request)
    return r

@app.task
def email_task(request):
    r = email(request)
    return r




