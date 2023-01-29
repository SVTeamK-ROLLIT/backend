from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer
import json

#상원님 시리얼라이저를 참고하여 작성
def UserSerializer(user_data):
    dic = {}
    dic['id'] = user_data.id
    dic['email'] = user_data.email
    dic['nickname'] = user_data.nickname
    return dic

def PaperSerializer(paper_data):
    dic = {}
    dic['user']=paper_data.user_id
    dic['id'] = paper_data.id
    dic['title'] = paper_data.title
    dic['paper_url'] = paper_data.paper_url
    dic['create_at'] = paper_data.create_at
    return dic

#짝퉁 시리어라이즈 : 딕셔너리로 만들어 줌
def memo_serializer(memo_queryset):
    dic = {}
    dic['memo_id'] = memo_queryset.id
    dic['content'] = memo_queryset.content
    dic['nickname'] = memo_queryset.nickname
    dic['password'] = memo_queryset.password
    dic['xcoor'] = memo_queryset.xcoor
    dic['ycoor'] = memo_queryset.ycoor
    # font_id = memo_queryset.font_id #memo에 있는 font_id를 가져옴
    # #그 아이디를 기준으로 폰트 컬럼(행)을 찾아서 font_type( ex)"안성탕면체")을 가져옴
    # font = Font.objects.get(pk=font_id).font_type 
    dic["font"] = memo_queryset.font
    dic["color"] = memo_queryset.color
    dic["font_color"]=memo_queryset.font_color
    
    #json이랑 dictionary랑 뭐가 다른지는 모르겠는데 JSON으로 만들어주는 느낌
    # json_dic = json.dumps(dic) 
    return dic #json_dic

def image_serializer(image_queryset):
    dic = {}
    dic['image_id'] = image_queryset.id
    dic['password'] = image_queryset.password
    dic['xcoor'] = image_queryset.xcoor
    dic['ycoor'] = image_queryset.ycoor
    dic['rotate'] = image_queryset.rotate
    #이미지 url을 가져와야해 폰트와 다르게 이미지 테이블에 url이 있어
    dic['image_url'] = image_queryset.image_url
    dic['width'] = image_queryset.width
    dic['height'] = image_queryset.height

    return dic

def sticker_serializer(sticker_queryset):
    dic = {}
    dic['sticker_id'] = sticker_queryset.id
    dic['password'] = sticker_queryset.password
    dic['xcoor'] = sticker_queryset.xcoor
    dic['ycoor'] = sticker_queryset.ycoor
    dic['rotate'] = sticker_queryset.rotate
    #스티커가 가지고 있는 스티커 저장소의 기본키를 가져온다
    sticker_id = sticker_queryset.default_sticker_id
    #그 기본키로 탐색해서 url을 가져온다
    sticker_url = DefaultSticker.objects.get(pk=sticker_id).sticker_url
    dic['sticker_url'] = sticker_url

    return dic

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','password')


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','nickname','password')

class MakePaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ('user', 'paper_url','title','id')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta: #paper_id는 views.py에서 입력받으므로 serializer에서는 넣지 않음
        model = Image
        fields = ('image_url','xcoor','ycoor','rotate','password')

class PhotoXySerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('xcoor','ycoor','width','height','rotate')

class MemoSerializer(serializers.ModelSerializer):
    class Meta: #paper_id는 views.py에서 입력받으므로 serializer에서는 넣지 않음
        model = Memo
        fields = ('content','nickname', 'font','color', 'font_color', 'password', 'xcoor','ycoor')

class MemoXySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('xcoor','ycoor')

class MemoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('id','password') # is_deleted는 views.py에서 자동 변환하므로 넣지 않아도 된다.

class StickerSerializer(serializers.ModelSerializer):
    class Meta: #paper_id는 views.py에서 입력받으므로 serializer에서는 넣지 않음
        model = Sticker
        fields = ('xcoor','ycoor','rotate','password')

class StickerXySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ('xcoor','ycoor')