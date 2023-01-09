from django.urls import path


from . import views

urlpatterns = [
    path('users/login', views.login),
    path('users/papers',views.paper), #롤링페이퍼 만들기
    path('users/signup',views.sign_up), 
    path('papers/<int:paper_id>/photos',views.photo),#사진 추가
    path('papers/<int:paper_id>/memos',views.memo), #메모 생성
    path('papers/<int:memo_id>',views.memo_delete), #메모 삭제
    path('papers/<int:paper_id>/stickers',views.stickers) #스티커를 추가
]
