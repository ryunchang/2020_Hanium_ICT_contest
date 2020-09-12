# -*- coding: utf-8 -*- 

import argparse
import numpy as np
import cv2
import tensorflow as tf
from  PIL import Image
import datetime
from time import time
from model import LPRNet
from loader import resize_and_normailze
from car_detecting import *
from plate_recognition import *

now=datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S ')

CFG = b"/home/yoon/hanium/darknet/cfg/yolov3.cfg"
WEIGHTS = b"/home/yoon/hanium/darknet/yolov3.weights"
DATA = b"/home/yoon/hanium/darknet/cfg/coco.data"
IMG = "/home/yoon/hanium/darknet/20200816_213508.jpg"

url = 'rtsp://admin:12341234!@192.168.1.108:554'

classnames = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "가", "나", "다", "라", "마", "거", "너", "더", "러",
              "머", "버", "서", "어", "저", "고", "노", "도", "로",
              "모", "보", "소", "오", "조", "구", "누", "두", "루",
              "무", "부", "수", "우", "주", "허", "하", "호"
              ]




def start() :
    img = cv2.imread(IMG, cv2.IMREAD_COLOR)
    height,width,channel  = img.shape

    car_images = extract_car_image(CFG, WEIGHTS, DATA, IMG)

    plate_list = {}
    for i in range(len(car_images)) :
        print(car_images[i][1])
        print(width/3)
        if car_images[i][1] < width/3 :
            plate_list[1] = plate_detection(car_images[i][0],height,width)
        elif car_images[i][1]  < width*2/3 :
            plate_list[2] = plate_detection(car_images[i][0],height,width)
        else :
            plate_list[3] = plate_detection(car_images[i][0],height,width)

    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--image", required=True, help="path to image file")
    parser.add_argument("-w", "--weights", required=True, help="path to weights file")
    args = vars(parser.parse_args())

    tf.compat.v1.enable_eager_execution()
    net = LPRNet(len(classnames) + 1)
    net.load_weights(args["weights"])

    if 1 in plate_list :
        img = plate_list[1]
        x = np.expand_dims(resize_and_normailze(img), axis=0)
        t = time()
        result = net.predict(x, classnames)
        print("첫번째 자동차 : ", result)
        print(time() - t)
        cv2.imshow("1", img)
        #cv2.waitKey(0)
        cv2.imwrite(str(nowDatetime)+"plate_"+str(result[0])+".png",img)
        #cv2.destroyAllWindows()

    if 2 in plate_list :
        img = plate_list[2]
        x = np.expand_dims(resize_and_normailze(img), axis=0)
        t = time()
        result = net.predict(x, classnames)
        print("두번째 자동차 : ", result)
        print(time() - t)
        cv2.imshow("2", img)
        cv2.imwrite(str(nowDatetime)+"plate_"+str(result[0])+".png",img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    if 3 in plate_list  :
        img = plate_list[3]
        x = np.expand_dims(resize_and_normailze(img), axis=0)
        t = time()
        result = net.predict(x, classnames)
        print("세번째 자동차 : ", result)
        print(time() - t)
        cv2.imshow("3", img)
        cv2.imwrite(str(nowDatetime)+"plate_"+str(result[0])+".png",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    start()