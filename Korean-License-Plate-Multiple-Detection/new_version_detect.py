from cv2 import  cv2
from  PIL import Image
import numpy as np
import datetime

now=datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d %H- %M-%S ')




img_color = cv2.imread("1234.jpg", cv2.IMREAD_COLOR)
img_color = cv2.resize(img_color,dsize=(2688,1520),interpolation=cv2. INTER_AREA)

height,width,channel = img_color.shape

copy_img=img_color.copy()

gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 3)
canny = cv2.Canny(blur, 100, 100)
contours,hierarchy = cv2.findContours(canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)


#box1은 번호판 크기 ,box2 는 번호판안의 숫자 크기
box1=[]
box2=[]

#신형 및 구형 번호판 비율을 고려하여 설정하였다. 
# 번호판 전체 크기를 고려하여 설정하였다. 거리에 맞추어 설정해야함 옛날 번호판은 인식 못하는걸 생각
NEW_CAR_ratio=9
OLD_CAR_ratio=2.5
MAX_plate_area=height*width*0.002
MIN_plate_area=1000

#번호판 안의 숫자의 최소크기, 너비 ,길이 ,비율 을 설정하였다.
NUM_MIN_AREA = 100
NUM_MIN_WIDTH, NUM_MIN_HEIGHT =2 , 8
NUM_MIN_RATIO , NUM_MAX_RATIO = 0.2 ,1 

# box1 box2 제조
for i in range(len(contours)):
    cnt=contours[i]
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    rect_area=w*h
    aspect_ratio1 = float(w)/h


    if (aspect_ratio1 <= NEW_CAR_ratio) and (aspect_ratio1>=OLD_CAR_ratio) and (rect_area>MIN_plate_area) and (rect_area<MAX_plate_area):

        cv2.rectangle(img_color,(x,y),(x+w, y+h), (0, 255,0), 1)
        box1.append(cv2.boundingRect(cnt))

    if (aspect_ratio1 >= NUM_MIN_RATIO) and (aspect_ratio1<=NUM_MAX_RATIO) and (rect_area >=NUM_MIN_AREA) :
        cv2.rectangle(img_color,(x,y),(x+w, y+h), (255, 0,0), 1)
        box2.append(cv2.boundingRect(cnt))


cv2.imwrite("boxing.jpg",img_color)

# box1 버블정렬
for i in range(len(box1)): 
     for j in range(len(box1)-(i+1)):
          if box1[j][0]>box1[j+1][0]:
               temp=box1[j]
               box1[j]=box1[j+1]
               box1[j+1]=temp


# box2 버블정렬
for i in range(len(box2)): 
     for j in range(len(box2)-(i+1)):
          if box2[j][0]>box2[j+1][0]:
               temp=box2[j]
               box2[j]=box2[j+1]
               box2[j+1]=temp


#box1 에서 겹치는 부분 제거  미완성 부분 추가적인 수정 필요
box3=[]
for i in range(len(box1)-1):
            
    if (box1[i][0]+box1[i][2]) <= (box1[i+1][0]+box1[i+1][2]) and (box1[i][0]+box1[i][2])>=(box1[i+1][0]) and (box1[i][1]+box1[i][3])<=(box1[i+1][1]+box1[i+1][3]) and (box1[i][1]+box1[i][3])>=(box1[i+1][1]) : 
        box1[i]=0
    else:        
        box3.append(box1[i])
box1=box3


# #번호판 인식과정 box1에서 box2에 있는게 5개 정도 포함이 되는 경우 번호판이라 칭함 # 중심으로 생각새헛 ㅗㅇㄹ
# select=[]
# for i in range(len(box1)):
#     count=0
#     for j in range(len(box2)):
#         if box1[i][0]<box2[j][0] and (box1[i][0]+box1[i][2])>box2[j][0] and box1[i][1]<box2[j][1]  and (box1[i][1]+box1[i][3])>box2[j][1] :
#             count=count+1
#     if count >=5:
#         select.append(i)


select=[]
for i in range(len(box1)):
    count=0
    for j in range(len(box2)):
        if box1[i][0]<box2[j][0]+box2[j][2]/2 and (box1[i][0]+box1[i][2])>box2[j][0]+box2[j][2]/2 and box1[i][1]<box2[j][1]+box2[j][3]/2  and (box1[i][1]+box1[i][3])>box2[j][1]+box2[j][3]/2 :
            count=count+1
    if count >=5:
        select.append(i)

# #번호판 겹칠때 설정 나중에 따로 수정 

# for i in range(len(select)-1):
#     if box1[select[i]][0] == box1[select[i+1]][0] or box1[select[i]][1] == box1[select[i+1]][1] or box1[select[i]][2] == box1[select[i+1]][2] or box1[select[i]][3] == box1[select[i+1]][3]:
#         select_temp.append(select[i])

select_temp=[]
cnt=[0,0,0]
#차량 인식 과정
for i in range(len(select)):
    if  box1[select[i]][0]<width*0.33:

        if cnt[0]==0:
        
            select_temp.append(select[i])
            cnt.append(1)
 
    elif box1[select[i]][0]<width*0.66:        
        if cnt[1]==0:
          
            select_temp.append(select[i])
            cnt.append(2)
 
    elif box1[select[i]][0]<width:
        if cnt[2]==0:
     
            select_temp.append(select[i])
            cnt.append(3)



select=select_temp


#번호판 출력과정 
number_plate=[]
for i in range(len(select)):
    number_plate.append(0)

for i in range(len(select)):
    number_plate[i]=(copy_img[box1[select[i]][1]        :     box1[select[i]][3]+      box1[select[i]][1]  ,        box1[select[i]][0]   :  box1[select[i]][0]  + box1[select[i]][2]                    ])
    cv2.imshow("show",number_plate[i])
    cv2.waitKey(0)

for i in range(len(select)):
    cv2.imwrite(str(nowDatetime)+"plate_"+str(cnt[i+3])+".jpg",number_plate[i])