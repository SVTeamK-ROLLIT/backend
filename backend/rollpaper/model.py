from django.db import models

class Memo(models.Model):
    paper=models.ForeignKey(paper,on_delete=models.CASCADE) #paper_id로 저장
    font=models.ForeignKey(font,on_delete=models.CASCADE) #폰트랑 색깔이 삭제되면 메모도 사라져
    color=models.ForeignKey(color,on_delete=models.CASCADE) #color_id로 저장
    content=models.CharField(max_length=200) 
    nickname=models.CharField(max_length=20) 
    xcoor=models.IntegerField() 
    ycoor=models.IntegerField() 
    rotate=models.IntegerField() 
    password=models.CharField(max_length=20) 
    create_at=models.DateTimeField() 
    update_at=models.DateTimeField() 
    is_deleted=models.IntegerField #혹은 models.BooleanField

class Paper(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE) #user_id로 저장
    backimage_url=models.URLField(max_length=100)
    title=models.CharField(max_length=20)
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()
    is_deleted=models.IntegerField() 

class Image(models.Model):
    paper=models.ForeignKey(paper,on_delete=models.CASCADE) #paper_id로 저장
    image_url=models.URLField(max_length=100)
    xcoor=models.IntegerField() 
    ycoor=models.IntegerField() 
    rotate=models.IntegerField() 
    password=models.CharField(max_length=20)
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()
    is_deleted=models.IntegerField() 


class User(models.Model):
    email=models.EmailField(max_length=100,unique=True) #유효한 이메일 주소인지 체크하는 필드, 체크하는데 EmailValidator를 사용
    nickname=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()
    is_deleted=models.IntegerField()

class Sticker(models.Model):
    paper=models.ForeignKey(paper,on_delete=models.CASCADE) #paper_id로 저장
    default_sticker_id=models.ForeignKey(default_sticker,on_delete=models.CASCADE)
    xcoor=models.IntegerField() 
    ycoor=models.IntegerField() 
    rotate=models.IntegerField() 

class Default_sticker(models.Model):
    sticker_url=models.URLField(max_length=100)

class Font(models.Model):
    font_type=models.CharField(max_length=20) 

class Color(models.Model):
    color_type=models.CharField(max_length=20) #16진수 코드는 문자인가?


