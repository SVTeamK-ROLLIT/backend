from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
import boto3
from botocore.client import Config
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from backend.settings import AWS_BUCKET_REGION, AWS_STORAGE_BUCKET_NAME
from .serializers import *
from django.core.cache    import cache
import logging
import time 

import cv2
import numpy as np
import urllib.request
import ssl #인증서
from celery.result import AsyncResult #셀러리가 안깔려 있어서 노랑
from .tasks import cartoon_task, email_task
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)



from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method="POST", request_body = LoginSerializer)
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

    
@swagger_auto_schema(method="POST", request_body = SignUpSerializer)
@api_view(['POST'])
def sign_up(request): #이메일을 UK로 지정해서 같은 이메일로 요청시 해당 데이터가 저장되었다가 삭제되는 것 같음.
    email = request.data['email'] #프론트에서 json 형식으로 다운 받은 데이터 중 [] 안에 있는 종류의 데이터를 변수에 저장
    password = request.data['password']
    nickname = request.data['nickname']
    
    if User.objects.filter(email=request.data['email']).exists():
        return JsonResponse({"message":"already signed email"}, status=400)
    elif User.objects.filter(nickname=request.data['nickname']).exists():
            return JsonResponse({"message": "already use nickname"}, status=400)
    else:
        result = User.objects.create(email = email, password = password, nickname = nickname) # 회원가입이 완료된 데이터
        user_id = result.id
        return JsonResponse({"user_id": user_id}, status=200)

@swagger_auto_schema(method="POST", request_body=MakePaperSerializer)
@api_view(['POST']) 
def paper(request, user_id):
    #TODO 1 프론트에서 정보 받아오기
    user = User.objects.get(pk=user_id)
    paper_url = request.data['paper_url']
    title = request.data['title']
    
    #TODO 2 user_id를 탐색키로 유저 객체 반환, 이거를 paper의 외래키로 넣어줘야 함
    #user = User.objects.get(pk=user_id)

    # #TODO 3 paper 테이블 Title로 탐색해서 같은 Title을 가지면 다른 제목을 입력해 주세요 반환
    # papers = Paper.objects.all()
    # if papers.filter(user=user).filter(title=title): #압력 받은 title이 이미 존재하면 "이미 있어요!" 반환
    #      return JsonResponse({"message": "already existing title"}, status=400)

    #TODO 4 paper 생성
    new_paper = Paper.objects.create(user=user, paper_url=paper_url, title=title)

    #TODO 5 paper_id를 JSON형식으로 만들기
    new_paper_id = {"paper_id":new_paper.id}
    return JsonResponse(new_paper_id, status=200)

@swagger_auto_schema(method="POST", request_body=PhotoSerializer)
@api_view(['POST']) 
def photo(request,paper_id):
    paper = Paper.objects.get(pk=paper_id) #paper_id는 url을 통해서 들어옴
    xcoor = request.data['xcoor']
    ycoor = request.data['ycoor']
    rotate = request.data['rotate']
    password = request.data['password']
    image = request.data['image'] # 우리가 DB에 저장할 때는 url을 넣어줄거야 url은 s3버킷에서 받아와
    width = request.data['width']
    height = request.data['height']

    #TODO 1 사진을 s3 버킷에 올리기
    s3=boto3.resource( #S3 버킷 등록하기
        's3',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        config = Config(signature_version='s3v4') #이건 뭘까
    )
    random_number = str(uuid.uuid4())
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=random_number, Body=image, ContentType='image/jpg')
   
    #TODO 2 사진 url을 받아옴
    image_url = f"https://sangwon-bucket.s3.ap-northeast-1.amazonaws.com/{random_number}"

    #TODO 3 DB에 저장
    new_photo = Image.objects.create(paper=paper, image_url=image_url, password=password,
    xcoor=xcoor, ycoor=ycoor, rotate=rotate, width=width, height=height)
    
    url = {"image_url":image_url}
    return JsonResponse(url, status=200)
    
@swagger_auto_schema(method="POST", request_body = MemoSerializer)
@api_view(['POST']) 
def memo(request,paper_id):
    paper = Paper.objects.get(pk=paper_id)
    # font = Font.objects.get(font_type=request.data['font']) #폰트랑 색깔이 삭제되면 메모도 사라져
    font = request.data['font'] #폰트랑 색깔이 삭제되면 메모도 사라져
    # color = Color.objects.get(color_type=request.data['color']) #color_id로 저장
    color = request.data['color'] #color_id로 저장
    # font_color = Color.objects.get(color_type=request.data['font_color'])
    font_color = request.data['font_color']
    content = request.data['content']
    nickname = request.data['nickname'] 
    password = request.data['password']
    xcoor = request.data['xcoor']
    ycoor = request.data['ycoor']
    #TODO 1 font랑 Color 테이블에 데이터 만들기(로컬에)

    #TODO 2 메모지 만들기 
    new_memo = Memo.objects.create(paper=paper, font=font, color=color, content=content,
    nickname=nickname, font_color = font_color, password=password, xcoor=xcoor, ycoor=ycoor)

    return JsonResponse({"memo_id": new_memo.id}, status=200)

# @swagger_auto_schema(method="POST", request_body = MemoXySerializer)
# @api_view(["POST"])
# def memo_xy(request, paper_id, memo_id):
#     #1. 메모 아이디 가져오기
#     memo = Memo.objects.get(pk=memo_id)
#     #2. 메모의 좌표값 입력받기
#     memo.xcoor = request.data['xcoor']
#     memo.ycoor = request.data['ycoor']
#     #3. 입력받은 좌표값을 DB에 저장
#     memo.save()

#     #4. 롤링페이퍼에 저장되어있는 메모, 스티커, 이미지 사진 모두 반환
#     memos = Memo.objects.filter(paper=paper_id, is_deleted=1).exclude(xcoor = None, ycoor=None)
#     all_memos = list(memos.values())
    
#     stickers = Sticker.objects.filter(paper=paper_id)
#     all_stickers = list(stickers.values())

#     images = Image.objects.filter(paper=paper_id)
#     all_images = list(images.values())

#     return JsonResponse({"all_memo": all_memos, "all_sticker":all_stickers, "all_images":all_images},status=200)

    
@swagger_auto_schema(method="POST", request_body = MemoDeleteSerializer)
@api_view(['POST']) 
def memo_delete(request, memo_id):
    #TODO 1: 메모지 가져오기
    memo = Memo.objects.get(pk=memo_id)
        
    #TODO 2: 입력한 비밀번호와 메모의 비밀번호가 일치하는지 확인
    if memo.password == request.data['password']:
        memo.is_deleted = 0 
        memo.save()
        return JsonResponse({"is_deleted":memo.is_deleted}, status=200)
    else:
        return JsonResponse({"message": "delete fail"}, status=400)

    #Postman으로 잘못된 비밀번호 입력 시 확인했고 
    #비밀번호 맞을 시 DB에서 is_deleted값이 0으로 변하는 것 확인했습니다


#구현방식 : 프론트에서 어느 페이퍼인지에대한 정보를 받아서 스티커에 저장한다.
@swagger_auto_schema(method="POST", request_body = StickerSerializer)
@api_view(['POST']) 
def stickers(request,paper_id):
    xcoor = request.data['xcoor']
    ycoor = request.data['ycoor']
    rotate = request.data['rotate']
    paper = Paper.objects.get(pk=paper_id)
    password = request.data['password']
    #스티커 저장소에서 스티커를 받아옴 여기에 스티커 url 있음
    default_sticker = DefaultSticker.objects.get(pk=request.data['default_sticker_id'])
    #스티커 컬럼을 만드는 재료로 스터커 저장소에서 가져온 객체가 필요(위의 변수)
    new_sticker = Sticker.objects.create(default_sticker=default_sticker, password=password, xcoor=xcoor, 
    ycoor=ycoor, rotate=rotate, paper=paper)
    return JsonResponse({"message": "sticker added"}, status=201)
    
    #실패하는 케이스는 생각을 못했고 사진을 가리면 안되는 느낌으로 추가구현하면 좋을 거 같습니다

@api_view(['GET'])
def my_page(request, user_id):
    dict={"user_data":[], "paper_data":[]}
    for user_data in User.objects.filter(id=user_id):
        json_user_part = UserSerializer(user_data)
        dict['user_data'].append(json_user_part)

    for paper_data in Paper.objects.filter(user=user_id):
        json_paper_part = PaperSerializer(paper_data)
        dict['paper_data'].append(json_paper_part)

    return JsonResponse(dict, safe=False)

@api_view(['GET'])
def get_paper(request,paper_id): #user_id는 쓰나?
    #TODO memo 먼저 하자
    dict={"title":"title", "paper_url":"paper_url","memo":[],"image":[],"sticker":[]}
    paper = Paper.objects.get(pk=paper_id)
    title = paper.title
    paper_url = paper.paper_url
    dict["title"] = title
    dict["paper_url"] = paper_url

    for memo in Memo.objects.filter(paper=paper_id, is_deleted=1).exclude(xcoor = None, ycoor=None): #아마 리스트 형식으로 쿼리셋을 반환할 거에요
        json_memo_part = memo_serializer(memo) #memo에서 필요한 정보를 JSON으로 바꿔줍니다
        #근데 JSON으로 바꾸려고 하니까 딕셔너리에 추가할 때 오류가 발생해서 그냥 dic으로 반환
        #memo의 value값에 방금 만든 json을 추가하여 수정해 줍니다
        dict["memo"].append(json_memo_part)
    
    for image in Image.objects.filter(paper=paper_id, is_deleted=1).exclude(xcoor = None, ycoor=None):
        json_image_part = image_serializer(image) #딕셔너리 만들기
        dict["image"].append(json_image_part) #원본에 추가
    
    for sticker in Sticker.objects.filter(paper_id=paper_id).exclude(xcoor = None, ycoor=None):
        json_sticker_part = sticker_serializer(sticker)
        dict["sticker"].append(json_sticker_part)
    
    #메모지의 위치가 지정되지 않아 null인 경우 롤링페이퍼 상에서 출력되지 않도록하기
    json_dict = json.dumps(dict, ensure_ascii=False)
    return JsonResponse(dict, safe=False )
    
@api_view(['GET'])
def get_stickers(request):
    start = time.time()
    #스티커 객체를 가져온다
    sticker_object = DefaultSticker.objects.all()
    sticker_dict={"data":[]}
    #sticker_list = []
    if not cache.get("sticker_list"):
        for sticker in sticker_object:
            sticker_info_dict ={"default_sticker_id":sticker.id,
            "sticker_url":sticker.sticker_url}
            sticker_dict['data'].append(sticker_info_dict)
            #sticker_list.append(sticker_info_dict)
        #Redis 부분
        cache.set("sticker_list",sticker_dict)
        sticker_data = cache.get("sticker_list")
        speed = time.time() -start
        speedlog = ">>>>>>>>>걸린시간>>>>>"+str(speed )
        logger.debug(speedlog)
        return JsonResponse(sticker_data, status=200, safe=False)

    #Redis 부분
    sticker_data = cache.get("sticker_list") #엄청 빨리 가져오는 거죠
    speed = time.time() -start
    speedlog = ">>>>>>>>>걸린시간>>>>>"+str(speed )
    logger.debug(speedlog)
    return JsonResponse(sticker_data, status=200, safe=False)

@api_view(['POST'])
def cartoon_id(request): 
    url = request.data["url"]
    task = cartoon_task.delay(url) #큐에 넣기?
    return_data = {"task_id":task.id}
    return JsonResponse(return_data, status=201)  

@api_view(['GET'])
def cartoon_result(request,task_id):
    task = AsyncResult(task_id) #작업 번호를 통해 작업상태 확인
    if not task.ready(): #아직 변환 완료 X
        return JsonResponse({'message':"still working"})
    #이게 뭐지? 일단 여기서 필터처리된 이미지url 받으면  좋을 거 같아
    data = task.get() # task의 return 값이지 않을까? 
    return JsonResponse(data,safe=False,status=201)

@api_view(['POST'])
def email_id(request):
    url = request.data["url"]
    email  =request.data["email"]
    data ={"url" : url, "email" : email}
    task = email_task.delay(data)
    return_data = {"task_id":task.id}
    return JsonResponse(return_data, status=201)

@csrf_exempt 
@api_view(['POST'])
def email_result(request):
    task_id = request.data['task_id']
    task = AsyncResult(task_id) #작업 번호를 통해 작업상태 확인
    if not task.ready(): #아직 변환 완료 X
        return JsonResponse({'message':"still working"})
    data = task.get() # task의 return 값이지 않을까? 
    return JsonResponse(data,safe=False,status=201)


@api_view(['POST']) 
def s3_upload(request):
    image = request.data['image'] # 우리가 DB에 저장할 때는 url을 넣어줄거야 url은 s3버킷에서 받아와
     #TODO 1 사진을 s3 버킷에 올리기
    s3=boto3.resource( #S3 버킷 등록하기
        's3',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        config = Config(signature_version='s3v4') #이건 뭘까
    )
    random_number = str(uuid.uuid4())
    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=random_number, Body=image, ContentType='image/jpg')
   
    #TODO 2 사진 url을 받아옴
    image_url = f"https://sangwon-bucket.s3.ap-northeast-1.amazonaws.com/{random_number}"
    
    url = {"url":image_url}
    return JsonResponse(url, status=200)

