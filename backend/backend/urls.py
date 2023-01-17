from django.contrib import admin
from django.urls import path,include


from rollpaper import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('rollpaper.urls')),
    #promethus
    path("", include("django_prometheus.urls"))
]
