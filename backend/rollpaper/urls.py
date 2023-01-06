from django.urls import path
from . import views

app_name = 'rollpaper'

urlpatterns = [
    path('users/signup', views.sign_up),
]