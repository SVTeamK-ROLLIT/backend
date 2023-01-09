from rest_framework import serializers
from .models import *

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','nickname','password','create_at','update_at','is_deleted']

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ('id', 'title','paper_url','create_at', 'is_deleted')

class MyPageSerializer(serializers.ModelSerializer):
   paper_id = PaperSerializer(many=True)
   class Meta:
        model = User
        field = ('id', 'email', 'nickname','paper_id')
