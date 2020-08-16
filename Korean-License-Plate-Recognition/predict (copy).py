# -*- coding: utf-8 -*- 

import argparse
from time import time

import numpy as np
import cv2
import tensorflow as tf
from  PIL import Image

from model import LPRNet
from loader import resize_and_normailze


classnames = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "가", "나", "다", "라", "마", "거", "너", "더", "러",
              "머", "버", "서", "어", "저", "고", "노", "도", "로",
              "모", "보", "소", "오", "조", "구", "누", "두", "루",
              "무", "부", "수", "우", "주", "허", "하", "호"
              ]


def detection() :
    img_color = cv2.imread('1234.jpg', cv2.IMREAD_COLOR)

    copy_img=img_color.copy()
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray, (3,3), 2)
    canny = cv2.Canny(blur, 100, 100)

    # contours로 같은에너지 네모박스
    #contours,hierarchy = cv2.findContours(canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    _, contours,_=cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    box1=[]

    f_count=0
    select=0
    plate_width=0

    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        rect_area=w*h
        aspect_ratio = float(w)/h

        if (aspect_ratio >= 0.2) and (aspect_ratio<=1.0) and (rect_area>=100) and (rect_area<=1200):
            cv2.rectangle(img_color,(x,y),(x+w, y+h), (0, 255,0), 1)
            box1.append(cv2.boundingRect(cnt))

    # 버블정렬
    for i in range(len(box1)): 
        for j in range(len(box1)-(i+1)):
            if box1[j][0]>box1[j+1][0]:
                temp=box1[j]
                box1[j]=box1[j+1]
                box1[j+1]=temp

    box1_1 = [[0 for j in range(4)] for i in range(len(box1))]
    box1_2 = [[0 for j in range(4)] for i in range(len(box1))]
    box1_3 = [[0 for j in range(4)] for i in range(len(box1))]

    for k in range(len(box1)):     
        if box1[k][0]<700:
            box1_1[k]=box1[k]
        elif box1[k][0]<1200:
            box1_2[k]=box1[k]
        elif box1[k][0]<1920:
            box1_3[k]=box1[k]

    box1=[box1_1,box1_2,box1_3]
    select=[0,0,0]

    for i in range(0,3):
        f_count=0
        for m in range(len(box1[i])):
            count=0
            for n in range(m+1,(len(box1[i])-1)):
                delta_x=abs(box1[i][n+1][0]-box1[i][m][0])
                if delta_x > 150:
                        break
                delta_y =abs(box1[i][n+1][1]-box1[i][m][1])
                if delta_x ==0:
                        delta_x=1
                if delta_y ==0:
                        delta_y=1           
                gradient =float(delta_y) /float(delta_x)
                        
                if gradient<0.25:
                        count=count+1
                    
            #measure number plate size         
            if count > f_count :
                f_count=count 
                select[i] = m
                plate_width=delta_x



    number_plate_1=copy_img[box1[0][select[0]][1]-10:box1[0][select[0]][3]+box1[0][select[0]][1]+5,box1[0][select[0]][0]-5:130+box1[0][select[0]][0]]
    number_plate_2=copy_img[box1[1][select[1]][1]-10:box1[1][select[1]][3]+box1[1][select[1]][1]+5,box1[1][select[1]][0]-5:130+box1[1][select[1]][0]]
    number_plate_3=copy_img[box1[2][select[2]][1]-10:box1[2][select[2]][3]+box1[2][select[2]][1]+5,box1[2][select[2]][0]-5:130+box1[2][select[2]][0]]

    return (number_plate_1, number_plate_2, number_plate_3)

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
    parser.add_argument("-i", "--image", required=True, help="path to image file")
    parser.add_argument("-w", "--weights", required=True, help="path to weights file")
    args = vars(parser.parse_args())

    tf.compat.v1.enable_eager_execution()
    net = LPRNet(len(classnames) + 1)
    net.load_weights(args["weights"])

    first, second, third = detection() 
    # img = cv2.imread(args["image"])

    # x = np.expand_dims(resize_and_normailze(img), axis=0)
    # t = time()
    # print(net.predict(x, classnames))
    # print(time() - t)
    # cv2.imshow("lp", img)
    # cv2.waitKey(0)
    img = first

    x = np.expand_dims(resize_and_normailze(img), axis=0)
    t = time()
    print(net.predict(x, classnames))
    print(time() - t)
    cv2.imshow("lp", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img = second

    x = np.expand_dims(resize_and_normailze(img), axis=0)
    t = time()
    print(net.predict(x, classnames))
    print(time() - t)
    cv2.imshow("lp", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img = third

    x = np.expand_dims(resize_and_normailze(img), axis=0)
    t = time()
    print(net.predict(x, classnames))
    print(time() - t)
    cv2.imshow("lp", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
