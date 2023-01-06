from django.http import JsonResponse
from django.shortcuts import render
from .models import User
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['POST']) 
def login(request):
    #TODO 1 POST로 값 받기
    user_email = request.data['email'] #여기에 받은 정보가 있어
    #TODO 2 데이터 베이스에서 email이 같은 컬럼 찾기 -> 못찾으면 오류
    users = User.objects.all() #유저 정보를 전부 가져옴
    try:
        if users.get(email=user_email): #email이 존재하면
            user_data = users.get(email=user_email) #user의 정보를 갖고 있는 컬럼 받기
    except:
        return JsonResponse({"message": "user not exist"}, status=400) #이메일이 DB에 존재하지 않음
    #해당 이메일로 탐색
    #TODO 3 해당 컬럼에서의 비밀번호와 입력받은 비밀번호 비교 -> 같으면 성공, 다르면 실패
    if user_data.password == request.data['password']:
        logindata = {"user_id":user_data.id}
        return JsonResponse(logindata, status=200)#user_id 정보 return 해줘 json으로
    else:
        return JsonResponse({"message": "incorrect password "}, status=400)

    