# -*- coding: utf-8 -*- 

import argparse
from time import time

import numpy as np
import cv2
import tensorflow as tf
from  PIL import Image
import datetime
from model import LPRNet
from loader import resize_and_normailze


classnames = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "가", "나", "다", "라", "마", "거", "너", "더", "러",
              "머", "버", "서", "어", "저", "고", "노", "도", "로",
              "모", "보", "소", "오", "조", "구", "누", "두", "루",
              "무", "부", "수", "우", "주", "허", "하", "호"
              ]


def detection() :
    now=datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H- %M-%S ')
    
    img_color = cv2.imread("1234.jpg", cv2.IMREAD_COLOR)
    img_color = cv2.resize(img_color,dsize=(2688,1520),interpolation=cv2. INTER_AREA)
    
    height,width,channel = img_color.shape
    
    copy_img=img_color.copy()
    
    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 3)
    canny = cv2.Canny(blur, 100, 100)
    _, contours,hierarchy = cv2.findContours(canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    
    
    #plate_box은 번호판 크기 ,number_box 는 번호판안의 숫자 크기
    plate_box=[]
    number_box=[]
    
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
    
    # plate_box, number_box 제조
    for i in range(len(contours)):
        cnt=contours[i]
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
    
    
    #plate_box 에서 겹치는 부분 제거  미완성 부분 추가적인 수정 필요
    #plate_box_temp=[]
    #for i in range(len(plate_box)-1):   
    #    if not (plate_box[i][0]+plate_box[i][2]) <= (plate_box[i+1][0]+plate_box[i+1][2]) and (plate_box[i][0]+plate_box[i][2])>=(plate_box[i+1][0]) and (plate_box[i][1]+plate_box[i][3])<=(plate_box[i+1][1]+plate_box[i+1][3]) and (plate_box[i][1]+plate_box[i][3])>=(plate_box[i+1][1]) :    
    #        plate_box_temp.append(plate_box[i])
    #        print(plate_box_temp)
    #plate_box=plate_box_temp
    
    # #번호판 인식과정 plate_box에서 number_box에 있는게 5개 정도 포함이 되는 경우 번호판이라 칭함 # 중심으로 생각새헛 ㅗㅇㄹ
    # valid_plate=[]
    # for i in range(len(plate_box)):
    #     count=0
    #     for j in range(len(number_box)):
    #         if plate_box[i][0]<number_box[j][0] and (plate_box[i][0]+plate_box[i][2])>number_box[j][0] and plate_box[i][1]<number_box[j][1]  and (plate_box[i][1]+plate_box[i][3])>number_box[j][1] :
    #             count=count+1
    #     if count >=5:
    #         valid_plate.append(i)
    
    
    valid_plate=[]
    for i in range(len(plate_box)):
        count=0
        for j in range(len(number_box)):
            if plate_box[i][0]<number_box[j][0]+number_box[j][2]/2 and (plate_box[i][0]+plate_box[i][2])>number_box[j][0]+number_box[j][2]/2 and plate_box[i][1]<number_box[j][1]+number_box[j][3]/2  and (plate_box[i][1]+plate_box[i][3])>number_box[j][1]+number_box[j][3]/2 :
                count=count+1
        if count >=5:
            valid_plate.append(i)
    
    # #번호판 겹칠때 설정 나중에 따로 수정 
    
    # for i in range(len(valid_plate)-1):
    #     if plate_box[valid_plate[i]][0] == plate_box[valid_plate[i+1]][0] or plate_box[valid_plate[i]][1] == plate_box[valid_plate[i+1]][1] or plate_box[valid_plate[i]][2] == plate_box[valid_plate[i+1]][2] or plate_box[valid_plate[i]][3] == plate_box[valid_plate[i+1]][3]:
    #         valid_plate_temp.append(valid_plate[i])

    valid_plate_temp=[]
    cnt=[0,0,0]
    #차량 인식 과정
    for i in range(len(valid_plate)):
        if  plate_box[valid_plate[i]][0]<width*0.33:
            if cnt[0]==0:
                valid_plate_temp.append(valid_plate[i])
                cnt[0] = 1
     
        elif plate_box[valid_plate[i]][0]<width*0.66:        
            if cnt[1]==0:
                valid_plate_temp.append(valid_plate[i])
                cnt[1] = 2
     
        elif plate_box[valid_plate[i]][0]<width:
            if cnt[2]==0:
                valid_plate_temp.append(valid_plate[i])
                cnt[2] = 3
    
    valid_plate=valid_plate_temp
    #번호판 출력과정 
    number_plate = {}
    for i in range(len(cnt)):
        if (cnt[i] != 0) :
            number_plate[i+1] =  (copy_img[plate_box[valid_plate[i]][1] : plate_box[valid_plate[i]][3]+ plate_box[valid_plate[i]][1], plate_box[valid_plate[i]][0] :  plate_box[valid_plate[i]][0]  + plate_box[valid_plate[i]][2] ])
    
    for i in range(len(cnt)):
        if not (cnt[i] == 0) :
            cv2.imshow("show",number_plate[i+1])
            cv2.waitKey(0)
    
    for i in range(len(cnt)):
        if not (cnt[i] == 0) :
            cv2.imwrite(str(nowDatetime)+"plate_"+str(cnt[i])+".png",number_plate[i+1])

    return number_plate

    # cv2.imshow('1', number_plate_1)
    # cv2.waitKey(0)
    # cv2.imwrite('plate1.jpg',number_plate_1)

    # cv2.imshow('2', number_plate_2)
    # cv2.waitKey(0)
    # cv2.imwrite('plate2.jpg',number_plate_2)

    # cv2.imshow('3', number_plate_3)
    # cv2.waitKey(0)
    # cv2.imwrite('plate3.jpg',number_plate_3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--image", required=True, help="path to image file")
    parser.add_argument("-w", "--weights", required=True, help="path to weights file")
    args = vars(parser.parse_args())

    tf.compat.v1.enable_eager_execution()
    net = LPRNet(len(classnames) + 1)
    net.load_weights(args["weights"])

    number_plate = detection() 
    # img = cv2.imread(args["image"])
    # x = np.expand_dims(resize_and_normailze(img), axis=0)
    # t = time()
    # print(net.predict(x, classnames))
    # print(time() - t)
    # cv2.imshow("lp", img)
    # cv2.waitKey(0)
    if 1 in number_plate :
        print("`1")
        img = number_plate[1]
        x = np.expand_dims(resize_and_normailze(img), axis=0)
        t = time()
        print(net.predict(x, classnames))
        print(time() - t)
        cv2.imshow("1", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if 2 in number_plate :
        img = number_plate[2]
        x = np.expand_dims(resize_and_normailze(img), axis=0)
        t = time()
        print(net.predict(x, classnames))
        print(time() - t)
        cv2.imshow("2", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if 3 in number_plate :
        img = number_plate[3]
        x = np.expand_dims(resize_and_normailze(img), axis=0)
        t = time()
        print(net.predict(x, classnames))
        print(time() - t)
        cv2.imshow("3", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
