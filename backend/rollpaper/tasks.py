#from __future__ import absolute_import,unicode_literals #이건 뭔데 둘 다 있지?
from backend.celery import app #앱을 가져와야 하나봐
from .views import cartoonize #원하는 함수 그냥 views에 만들어서 가져와야지

#비동기 작업 실시 
@app.task
def cartoonize(request): #request에 뭐가 들어가는 거지?
    r = cartoonize(request)
    return r 





