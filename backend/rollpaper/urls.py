from django.urls import path, include
from . import views


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.http import HttpResponse

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="TeamK Api",
        default_version='v1',
        description = '''
        익명 롤링페이퍼 서비스
        ''',
        terms_of_service="", # 서비스 주소?
        contact=openapi.Contact(email="teamk@email.com"), #옵션 / 개발자 연락처
        license=openapi.License(name="BSD License"), # 옵션 / MIT와 BSD 모두 유사한 내용을 명시해둔 라이센스, 참고 : https://selfish-developer.com/entry/오픈소스-라이센스-정리
    ),
    public = True,
    permission_classes = (permissions.AllowAny,),
)

urlpatterns = [
    path('users/login', views.login),
    path('users/<int:user_id>/papers',views.paper), #롤링페이퍼 만들기 <int:user_id> 추가함.
    path('users/signup',views.sign_up), #회원가입
    path('papers/<int:paper_id>/photos',views.photo),#사진 추가
    path('papers/<int:paper_id>/xyphotos',views.xyphotos), #image 정보들 null값인거 채워넣기
    path('papers/<int:paper_id>/memos',views.memo), #메모 생성
    path('papers/memos/<int:memo_id>',views.memo_delete), #메모 삭제
    path('papers/<int:paper_id>/stickers',views.stickers), #스티커를 추가
    path('users/<int:user_id>', views.my_page, name="my_page"), #user_id라는 것이 존재x, User 테이블의 id를 입력받음
    path('papers/<int:paper_id>/',views.get_paper), #paper의 memo,image,sticker의 정보를 가져옵니다
    path('papers/cartoons',views.cartoon_id),
    path('papers/sticker_list',views.get_stickers), #스티커 가져오기
    #path('papers/<int:paper_id>/<int:memo_id>/memoxy/', views.memo_xy), # 메모의 x, y좌표 정하기 #주소 끝에 '/'를 넣지 않으면 정상작동하지 않음
    path('papers/cartoons/results/<str:task_id>/<int:paper_id>',views.cartoon_result),
    path('users/papers/emails',views.email_id),
    path('users/papers/emails/results',views.email_result),
    path('photos',views.s3_upload), #s3에 이미지파일 올리면 url반환
    path('papers/images/<int:image_id>',views.image_delete),
    path('papers/stickers/<int:sticker_id>',views.sticker_delete)
]

if settings.DEBUG:
    urlpatterns += [
        path('swagger<str:format>', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('docs/', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


