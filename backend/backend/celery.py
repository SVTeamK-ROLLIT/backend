#celery.py, setting 옆에 있어
import os
from celery import Celery
from django.conf import settings #이건 뭘 가져오는 걸까?
#기본 장고파일 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings') #왼쪽은 고정 ,오른쪽은 프로젝트명.settings

 # celery와 rabbitMQ를 연결해 주는 부분같아
 # backend 부분이 없으면 Task의 실행 결과를 받을 수 없다고
app = Celery('backend', backend='redis://redis:6379', brocker='amqp://rabbitmq:5672') #app.Celery('프로젝트명')
#메모리 누수 문제 해결?
app.conf.worker_max_tasks_per_child = 100
app.config_from_object('django.conf:settings', namespace='CELERY') 
#설치된 모든 앱에서 자동으로 task를 찾게해줌
app.autodiscover_tasks()