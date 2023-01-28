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


# class Font(models.Model):
#     font_type = models.CharField(max_length=20) 

# class Color(models.Model):
#     color_type = models.CharField(max_length=20) #16진수 코드는 문자인가?

class Memo(models.Model):
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE) #paper_id로 저장
    # font = models.ForeignKey(Font,on_delete=models.CASCADE) #폰트랑 색깔이 삭제되면 메모도 사라져
    # color = models.ForeignKey(to = Color, related_name='color',on_delete=models.CASCADE,verbose_name='메모지색',default='') #color_id로 저장
    # font_color = models.ForeignKey(to = Color,related_name='font_color',on_delete=models.CASCADE,verbose_name='글씨색',default='')
    font = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    font_color = models.CharField(max_length=50)
    content = models.CharField(max_length=200) 
    nickname = models.CharField(max_length=100) 
    xcoor = models.IntegerField(null=True) 
    ycoor = models.IntegerField(null=True) 
    #rotate = models.IntegerField() 
    password = models.CharField(max_length=20) 
    create_at = models.DateTimeField(auto_now_add=True) 
    update_at = models.DateTimeField(auto_now=True) 
    is_deleted = models.IntegerField(default=1) #혹은 models.BooleanField



class Image(models.Model):
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE) #paper_id로 저장
    image_url = models.URLField(max_length=200) #블로그 참고로 imageFiled -> FileField로 수정
    # JSON으로 만들 때 에러나서 다시 FileField에서 URLField로 수정
    xcoor = models.IntegerField(default=0) 
    ycoor = models.IntegerField(default=0) 
    rotate = models.IntegerField(default=0) 
    password = models.CharField(max_length=20,default=0) 
    create_at = models.DateTimeField(auto_now_add=True) 
    update_at = models.DateTimeField(auto_now=True) 
    is_deleted = models.IntegerField(default=1) 
    width = models.IntegerField(null=True, default=200) 
    height = models.IntegerField(null=True,default=100) 

class DefaultSticker(models.Model):
    sticker_url = models.URLField(max_length=500) #url이 너무 길어서 글자 제한 늘림

class Sticker(models.Model):
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE) #paper_id로 저장
    default_sticker = models.ForeignKey(DefaultSticker,on_delete=models.CASCADE) #id를 빼줌
    xcoor = models.IntegerField() 
    ycoor = models.IntegerField() 
    rotate = models.IntegerField() 
    password = models.CharField(max_length=20, null=True, default='') #구현하면서 추가
    create_at = models.DateTimeField(auto_now_add=True, null=False) 
    update_at = models.DateTimeField(auto_now=True, null=False) 
    is_deleted = models.IntegerField(default=1) 
