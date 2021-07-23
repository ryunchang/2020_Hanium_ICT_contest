#-*- coding:utf-8 -*-
import cv2
import numpy as np
from  PIL import Image


img_color = cv2.imread('1234.jpg', cv2.IMREAD_COLOR)
copy_img=img_color.copy()
cv2.namedWindow('Show Image')
cv2.imshow('Show Image', img_color)
cv2.waitKey(0)

img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
cv2.imshow('Show Image', img_gray)
cv2.waitKey(0)

blur = cv2.GaussianBlur(img_gray, (3,3), 2)
cv2.imshow('Show Image', blur)
cv2.waitKey(0)

canny = cv2.Canny(blur, 100, 100)
cv2.imshow('Show Image', canny)
cv2.waitKey(0)




# contours로 같은에너지 네모박스
contours,hierarchy = cv2.findContours(canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

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

cv2.imshow('Show Image', img_color)
cv2.waitKey(0)




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
     if box1[k][0]<450:

          box1_1[k]=box1[k]
   
     elif box1[k][0]<800:

          box1_2[k]=box1[k]

     elif box1[k][0]<1400:

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



print(select)






#select를 찾으면 f_count를 초기화 시킬 필요가 있다고 생각이됩
#5 29 54

#print(s1,s2,s3)






number_plate_1=copy_img[box1[0][select[0]][1]-10:box1[0][select[0]][3]+box1[0][select[0]][1]+5,box1[0][select[0]][0]-5:130+box1[0][select[0]][0]]
     
     
number_plate_2=copy_img[box1[1][select[1]][1]-10:box1[1][select[1]][3]+box1[1][select[1]][1]+5,box1[1][select[1]][0]-5:130+box1[1][select[1]][0]]
     
     
number_plate_3=copy_img[box1[2][select[2]][1]-10:box1[2][select[2]][3]+box1[2][select[2]][1]+5,box1[2][select[2]][0]-5:130+box1[2][select[2]][0]]
     
     
cv2.imshow('1', number_plate_1)
cv2.waitKey(0)
cv2.imwrite('plate1.jpg',number_plate_1)

cv2.imshow('2', number_plate_2)
cv2.waitKey(0)
cv2.imwrite('plate2.jpg',number_plate_2)

cv2.imshow('3', number_plate_3)
cv2.waitKey(0)
cv2.imwrite('plate3.jpg',number_plate_3)




'''

# 사이즈 배율 조절
resize_plate=cv2.resize(number_plate,None,fx=5,fy=5,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR) 
cv2.imshow('Show Image', resize_plate)
cv2.waitKey(0)
cv2.imwrite('resize_plate.jpg',resize_plate)











#Gray 스캐줄로 변경
plate_gray=cv2.cvtColor(resize_plate,cv2.COLOR_BGR2GRAY)
cv2.imshow('Show Image', plate_gray)
cv2.waitKey(0)


# 가우시안 블러
blur = cv2.GaussianBlur(plate_gray, (3,3), 15)
cv2.imshow('Show Image', blur)
cv2.waitKey(0)


#  흑백으로 변환
ret,th_plate = cv2.threshold(blur,150,255,cv2.THRESH_BINARY)
cv2.imshow('Show Image', th_plate)
cv2.waitKey(0)

cv2.imwrite('plate_th.jpg',th_plate)


# 글자색 찐하게
kernel = np.ones((3,3),np.uint8)
er_plate = cv2.erode(th_plate,kernel,iterations=2)
cv2.imshow('Show Image', er_plate)
cv2.waitKey(0)




cv2.imwrite('savedimage.jpg', img_gray)
cv2.destroyAllWindows()
'''
