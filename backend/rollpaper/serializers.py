import json
from .models import*

#짝퉁 시리어라이즈 : 딕셔너리로 만들어 줌
def memo_serializer(memo_queryset):
    dic = {}
    dic['content'] = memo_queryset.content
    dic['nickname'] = memo_queryset.nickname
    dic['password'] = memo_queryset.password
    dic['xcoor'] = memo_queryset.xcoor
    dic['ycoor'] = memo_queryset.ycoor
    dic['rotate'] = memo_queryset.rotate
    font_id = memo_queryset.font_id #memo에 있는 font_id를 가져옴
    #그 아이디를 기준으로 폰트 컬럼(행)을 찾아서 font_type( ex)"안성탕면체")을 가져옴
    font = Font.objects.get(pk=font_id).font_type 
    dic["font"] = font
    
    #json이랑 dictionary랑 뭐가 다른지는 모르겠는데 JSON으로 만들어주는 느낌
    # json_dic = json.dumps(dic) 
    return dic #json_dic

def image_serializer(image_queryset):
    dic = {}
    dic['password'] = image_queryset.password
    dic['xcoor'] = image_queryset.xcoor
    dic['ycppr'] = image_queryset.ycoor
    dic['rotate'] = image_queryset.rotate
    #이미지 url을 가져와야해 폰트와 다르게 이미지 테이블에 url이 있어
    dic['image_url'] = image_queryset.image_url

    return dic

def sticker_serializer(sticker_queryset):
    dic = {}
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