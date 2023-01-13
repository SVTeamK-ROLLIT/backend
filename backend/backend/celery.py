#celery.py, setting 옆에 있어
import os
from celery import Celery
from django.conf import settings #이건 뭘 가져오는 걸까?
#기본 장고파일 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings') #왼쪽은 고정 ,오른쪽은 프로젝트명.settings
 
 # celery와 rabbitMQ를 연결해 주는 부분같아
app = Celery('backend', brocker='amqp://rabbitmq:5672') #app.Celery('프로젝트명')
#이건 모르겠어
app.config_from_object('django.conf:settings', namespace='CELERY') 
#등록된 장고 앱 설정에서 task 불러오기(우리가 실행시킬 함수를 불러 오는 건가?), 비동기 처리 시작?
app.autodiscover_tasks()