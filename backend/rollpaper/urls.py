from django.urls import path


from . import views

urlpatterns = [
    path('users/login', views.login),
    path('users/papers',views.paper),
    path('users/signup',views.sign_up),
    path('papers/<int:paper_id>/photos',views.photo),
    path('papers/<int:paper_id>/memos',views.memo)
]
