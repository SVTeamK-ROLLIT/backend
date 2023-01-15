import cv2
import numpy as np
import urllib.request
import ssl #인증서
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from backend.settings import AWS_BUCKET_REGION, AWS_STORAGE_BUCKET_NAME
import boto3
from botocore.client import Config
import uuid



#만화필터
def cartoonizer(requset): #셀러리에서 작업하는 부분
    #url로 받아와서 이미지 저장하는 부분
    url = requset
    #return JsonResponse(url1, status=200,safe = False) 
    context = ssl._create_unverified_context()
    resp = urllib.request.urlopen(url,context=context)
    image = np.asarray(bytearray(resp.read()), dtype='uint8')
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)

    line_size = 9
    blur_value = 5
    #edge_mask 선따기
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

    #색 갯수 정하기
    total_color = 9 
    # Transform the image
    data = np.float32(img).reshape((-1, 3))
    # Determine criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    # Implementing K-Means
    ret, label, center = cv2.kmeans(data, total_color, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    color_img = result


    blurred = cv2.bilateralFilter(color_img, d=7, sigmaColor=200,sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred,blurred,mask=edges)
    #numpy array를 image로 변환
    data_serial = cv2.imencode('.png', cartoon)[1].tobytes()

    #TODO 1 사진을 s3 버킷에 올리기
    s3=boto3.resource( #S3 버킷 등록하기
        's3',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        config = Config(signature_version='s3v4') #이건 뭘까
    )

    #이름 뽑아내기
    #img_name = "cartoon" + requset[55:]
    
    random_number = str(uuid.uuid4())

    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=random_number, Body=data_serial, ContentType='image/png')

    image_url = f"https://sangwon-bucket.s3.ap-northeast-1.amazonaws.com/{random_number}"

    cv2.waitKey()  
    cv2.destroyAllWindows() 
    dictionary = {"url":image_url}
    return dictionary
    






