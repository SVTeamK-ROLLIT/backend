from django.shortcuts import render
from rollpaper.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['POST'])
def sign_up(request):
    email = request.data['email']
    password = request.data['password']
    nickname = request.data['nickname']
    result = User.objects.create(email = email, password = password, nickname = nickname)
    user_id = result.id 
    return JsonResponse({"user_id": user_id}, status=200)
