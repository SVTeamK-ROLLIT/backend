from django.http import JsonResponse
from django.shortcuts import render
from .models import User, Paper, Image, Font, Color, Memo, DefaultSticker, Sticker
from rest_framework.decorators import api_view
import boto3
from botocore.client import Config
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from backend.settings import AWS_BUCKET_REGION, AWS_STORAGE_BUCKET_NAME
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


@api_view(['POST']) 
def paper(request):
    #TODO 1 프론트에서 정보 받아오기
    user_id = request.data['user_id']
    paper_url = request.data['paper_url']
    title = request.data['title']
    
    #TODO 2 user_id를 탐색키로 유저 객체 반환, 이거를 paper의 외래키로 넣어줘야 함
    user = User.objects.get(pk=user_id)

    # #TODO 3 paper 테이블 Title로 탐색해서 같은 Title을 가지면 다른 제목을 입력해 주세요 반환
    # papers = Paper.objects.all()
    # if papers.filter(user=user).filter(title=title): #압력 받은 title이 이미 존재하면 "이미 있어요!" 반환
    #      return JsonResponse({"message": "already existing title"}, status=400)
    

    #TODO 4 paper 생성
    new_paper = Paper.objects.create(user=user, paper_url=paper_url, title=title)

    #TODO 5 paper_id를 JSON형식으로 만들기
    new_paper_id = {"paper_id":new_paper.id}
    return JsonResponse(new_paper_id, status=200)

@api_view(['POST']) 
def photo(request,paper_id):
    paper = Paper.objects.get(pk=paper_id) #paper_id는 url을 통해서 들어옴
    xcoor = request.data['xcoor']
    ycoor = request.data['ycoor']
    rotate = request.data['rotate']
    password = request.data['password']
    image = request.data['image'] # 우리가 DB에 저장할 때는 url을 넣어줄거야 url은 s3버킷에서 받아와

    #TODO 1 사진을 s3 버킷에 올리기
    s3=boto3.resource( #S3 버킷 등록하기
        's3',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        config = Config(signature_version='s3v4') #이건 뭘까
    )
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=image.name, Body=image, ContentType='image/jpg')
   
    #TODO 2 사진 url을 받아옴
    image_url = f"https://sangwon-bucket.s3.ap-northeast-1.amazonaws.com/{image.name}"

    #TODO 3 DB에 저장
    new_photo = Image.objects.create(paper=paper, image_url=image_url, password=password,
    xcoor=xcoor, ycoor=ycoor, rotate=rotate)
    
    url = {"image_url":image_url}
    return JsonResponse({"message": "photo added"}, status=200)
    
@api_view(['POST']) 
def memo(request,paper_id):
    paper = Paper.objects.get(pk=paper_id)
    font = Font.objects.get(font_type=request.data['font']) #폰트랑 색깔이 삭제되면 메모도 사라져
    color = Color.objects.get(color_type=request.data['color']) #color_id로 저장
    content = request.data['content']
    nickname = request.data['nickname'] 
    xcoor = request.data['xcoor']
    ycoor = request.data['ycoor'] 
    rotate = request.data['rotate'] 
    password = request.data['password']
    #TODO 1 font랑 Color 테이블에 데이터 만들기(로컬에)

    #TODO 2 메모지 만들기
    new_memo = Memo.objects.create(paper=paper, font=font, color=color, content=content,
    nickname=nickname, xcoor=xcoor, ycoor=ycoor, rotate=rotate, password=password)

    return JsonResponse({"message": "memo created"}, status=200)
    
    
@api_view(['POST']) 
def memo_delete(request,memo_id):
    #TODO 1: 메모지 가져오기
    memo = Memo.objects.get(pk=memo_id)
        
    #TODO 2: 입력한 비밀번호와 메모의 비밀번호가 일치하는지 확인
    if memo.password == request.data['password']:
        memo.is_deleted = 0 
        memo.save()
        return JsonResponse({"message": "memo created","is_deleted":memo.is_deleted
        }, status=200)
    else:
        return JsonResponse({"message": "delete fail"}, status=400)

    #Postman으로 잘못된 비밀번호 입력 시 확인했고 
    #비밀번호 맞을 시 DB에서 is_deleted값이 0으로 변하는 것 확인했습니다

