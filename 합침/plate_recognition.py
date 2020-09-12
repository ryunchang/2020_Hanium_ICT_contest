# -*- coding: utf-8 -*- 

import cv2
import datetime

now=datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S ')



# 번호판 박스의 비율. 신형 및 구형 번호판 비율을 고려하여 설정
NEW_CAR_ratio = 9
OLD_CAR_ratio = 1.5

# 숫자 박스의 비율을 설정하였다.
NUM_MIN_RATIO , NUM_MAX_RATIO = 0.2 , 1 


def plate_detection(img_color, height, width) :

    #img_color = cv2.resize(img_color,dsize=(2688,1520),interpolation=cv2. INTER_AREA)

    MAX_plate_area = 30000#height * width / 18
    MIN_plate_area = 2000#height * width / 61
    NUM_MIN_AREA = 100 #height * width / 100

    copy_img=img_color.copy()
    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1,1), 3)
    canny = cv2.Canny(blur, 250, 300)

    _, contours, hierarchy = cv2.findContours(canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    #plate_box은 번호판 크기 ,number_box 는 번호판안의 숫자 크기
    plate_box=[]
    number_box=[]
    
    # plate_box, number_box 제조
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        rect_area=w*h
        aspect_ratio1 = float(w)/h
    
        if (aspect_ratio1 <= NEW_CAR_ratio) and (aspect_ratio1>=OLD_CAR_ratio) and (rect_area>MIN_plate_area) and (rect_area<MAX_plate_area):
            cv2.rectangle(img_color,(x,y),(x+w, y+h), (0, 255,0), 1)
            plate_box.append(cv2.boundingRect(cnt))
    
        if (aspect_ratio1 >= NUM_MIN_RATIO) and (aspect_ratio1<=NUM_MAX_RATIO) and (rect_area >=NUM_MIN_AREA) :
            cv2.rectangle(img_color,(x,y),(x+w, y+h), (255, 0,0), 1)
            number_box.append(cv2.boundingRect(cnt))
    
    cv2.imwrite(str(nowDatetime)+"box.png", img_color)
    #cv2.imshow("plate_box and number_box", img_color)

    # plate_box 버블정렬
    for i in range(len(plate_box)): 
         for j in range(len(plate_box)-(i+1)):
              if plate_box[j][0]>plate_box[j+1][0]:
                   temp=plate_box[j]
                   plate_box[j]=plate_box[j+1]
                   plate_box[j+1]=temp
    
    # number_box 버블정렬
    for i in range(len(number_box)): 
         for j in range(len(number_box)-(i+1)):
              if number_box[j][0]>number_box[j+1][0]:
                   temp=number_box[j]
                   number_box[j]=number_box[j+1]
                   number_box[j+1]=temp
    
    # plate 박스 안 number 박스들의 개수 측정
    valid_plate=[]
    for i in range(len(plate_box)):
        count = 0
        for j in range(len(number_box)):
            if plate_box[i][0]<number_box[j][0]+number_box[j][2]/2 and (plate_box[i][0]+plate_box[i][2])>number_box[j][0]+number_box[j][2]/2 and plate_box[i][1]<number_box[j][1]+number_box[j][3]/2  and (plate_box[i][1]+plate_box[i][3])>number_box[j][1]+number_box[j][3]/2 :
                count=count+1
        if count >=5:
            valid_plate.append(i)

    #번호판 사진 출력과정 
    if len(valid_plate) == 0 : 
        number_plate = None
    else :
        for i in range(len(valid_plate)):
            number_plate = (copy_img[plate_box[valid_plate[i]][1] : plate_box[valid_plate[i]][3]+ plate_box[valid_plate[i]][1], plate_box[valid_plate[i]][0] :  plate_box[valid_plate[i]][0]  + plate_box[valid_plate[i]][2] ])
    
    return number_plate