# 모델  세이브


from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=100,unique=True) #유효한 이메일 주소인지 체크하는 필드, 체크하는데 EmailValidator를 사용
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)

    update_at = models.DateTimeField(auto_now=True) #나중에 문제 생기면 null=False 검색 ㄱㄱ
    is_deleted = models.IntegerField(default=1) #0은 삭제된 상태로 가정


class Paper(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) #user_id로 저장
    paper_url = models.URLField(max_length=100)
    title = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.IntegerField(default=1) 


class Font(models.Model):
    font_type = models.CharField(max_length=20) 

class Color(models.Model):
    color_type = models.CharField(max_length=20) #16진수 코드는 문자인가?

class Memo(models.Model):
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE) #paper_id로 저장
    font = models.ForeignKey(Font,on_delete=models.CASCADE) #폰트랑 색깔이 삭제되면 메모도 사라져
    color = models.ForeignKey(Color,on_delete=models.CASCADE) #color_id로 저장
    content = models.CharField(max_length=200) 
    nickname = models.CharField(max_length=20) 
    xcoor = models.IntegerField() 
    ycoor = models.IntegerField() 
    rotate = models.IntegerField() 
    password = models.CharField(max_length=20) 
    create_at = models.DateTimeField(auto_now_add=True) 
    update_at = models.DateTimeField(auto_now=True) 
    is_deleted = models.IntegerField(default=1) #혹은 models.BooleanField



class Image(models.Model):
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE) #paper_id로 저장
    image_url = models.URLField(max_length=100)
    xcoor = models.IntegerField() 
    ycoor = models.IntegerField() 
    rotate = models.IntegerField() 
    password = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_deleted = models.IntegerField(default=1) 

class DefaultSticker(models.Model):
    sticker_url = models.URLField(max_length=100)

class Sticker(models.Model):
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE) #paper_id로 저장
    default_sticker_id = models.ForeignKey(DefaultSticker,on_delete=models.CASCADE)
    xcoor = models.IntegerField() 
    ycoor = models.IntegerField() 
    rotate = models.IntegerField() 
