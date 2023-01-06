from django.shortcuts import render
from rollpaper.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['POST'])
def sign_up(request): #이메일을 UK로 지정해서 같은 이메일로 요청시 해당 데이터가 저장되었다가 삭제되는 것 같음.
    email = request.data['email'] #프론트에서 json 형식으로 다운 받은 데이터 중 [] 안에 있는 종류의 데이터를 변수에 저장
    password = request.data['password']
    nickname = request.data['nickname']
    
    if User.objects.filter(email=request.data['email']).exists():
        return JsonResponse({"message":"already signed email"}, status=204)
    elif User.objects.filter(nickname=request.data['nickname']).exists():
            return JsonResponse({"message": "already use nickname"})
    else:
        result = User.objects.create(email = email, password = password, nickname = nickname) # 회원가입이 완료된 데이터
        user_id = result.id
        return JsonResponse({"user_id": user_id}, status=200)
