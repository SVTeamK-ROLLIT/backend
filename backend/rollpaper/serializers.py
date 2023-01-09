from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer

#상원님 시리얼라이저를 참고하여 작성
def UserSerializer(user_data):
    dic = {}
    dic['id'] = user_data.id
    dic['email'] = user_data.email
    dic['nickname'] = user_data.nickname
    return dic

def PaperSerializer(paper_data):
    dic = {}
    dic['id'] = paper_data.id
    dic['title'] = paper_data.title
    dic['paper_url'] = paper_data.paper_url
    dic['create_at'] = paper_data.create_at
    return dic