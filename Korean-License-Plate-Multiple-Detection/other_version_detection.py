def detaction():
    now=datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S ')


    #해상도가 높은 이미지를 불러오면 resize 과정중에 지연이 되거나 에러가 생김  되도록 정사이즈 ㄱㄱ
    img_color = cv2.imread("1234.jpg", cv2.IMREAD_COLOR)
    img_color = cv2.resize(img_color,dsize=(2016,1140),interpolation=cv2. INTER_AREA)

    height,width,channel = img_color.shape

    #화면 capture용 이미지입니다. 
    copy_img=img_color.copy()

    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)


    # 되도록 번호판 정도의 컨튜어를 찾는 과정
    #===============================================================================
    img_thresh = cv2.adaptiveThreshold(
        img_blurred, 
        maxValue=255.0, 
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        thresholdType=cv2.THRESH_BINARY_INV, 
        blockSize=19, 
        C=9
    )



    _,contours,hierarchy  = cv2.findContours(
    img_thresh, 
        mode=cv2.RETR_LIST, 
        method=cv2.CHAIN_APPROX_SIMPLE
    )



    temp_result = np.zeros((height, width, channel), dtype=np.uint8)
    contours_dict = []



    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
    #  cv2.rectangle(temp_result, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)
        
        # insert to dict
        contours_dict.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),
            'cy': y + (h / 2)
        })

    #번호판 글자의 크기, 최소 길이, 비율
    MIN_AREA = 80
    MIN_WIDTH, MIN_HEIGHT = 2, 8
    MIN_RATIO, MAX_RATIO = 0.25, 1
    MAX_AREA=500

    possible_contours = []

    #번호판 처럼 보이는 애들 남기
    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']
        ratio = d['w'] / d['h']

        
        if area > MIN_AREA \
        and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
        and MIN_RATIO < ratio < MAX_RATIO and  area <MAX_AREA:
            d['idx'] = cnt
            cnt += 1
            possible_contours.append(d)
        


    # visualize possible contours 좀더 정확하게 순차적 정렬 확인

    # for d in possible_contours:
    #  #   cv2.drawContours(temp_result, d['contour'], -1, (255, 255, 255))
    #     cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)

    #값을 바꾸어가면 생각 탄젠트 세타로 생각 차이들임
    MAX_DIAG_MULTIPLYER = 5 # 5
    MAX_ANGLE_DIFF = 12.0 # 12.0
    MAX_AREA_DIFF = 0.5 # 0.5
    MAX_WIDTH_DIFF = 0.8
    MAX_HEIGHT_DIFF = 0.2
    MIN_N_MATCHED = 3 # 3

    def find_chars(contour_list):
        matched_result_idx = []
        for d1 in contour_list:
            matched_contours_idx = []
            for d2 in contour_list:
                if d1['idx'] == d2['idx']:
                    continue
                dx = abs(d1['cx'] - d2['cx'])
                dy = abs(d1['cy'] - d2['cy'])
                diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)
                distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
                if dx == 0:
                    angle_diff = 90
                else:
                    angle_diff = np.degrees(np.arctan(dy / dx))
                area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
                width_diff = abs(d1['w'] - d2['w']) / d1['w']
                height_diff = abs(d1['h'] - d2['h']) / d1['h']
                if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                    matched_contours_idx.append(d2['idx'])
            # append this contour
            matched_contours_idx.append(d1['idx'])
            if len(matched_contours_idx) < MIN_N_MATCHED:
                continue
            matched_result_idx.append(matched_contours_idx)
            unmatched_contour_idx = []
            for d4 in contour_list:
                if d4['idx'] not in matched_contours_idx:
                    unmatched_contour_idx.append(d4['idx'])
            unmatched_contour = np.take(possible_contours, unmatched_contour_idx)
            # recursive
            recursive_contour_list = find_chars(unmatched_contour)
            for idx in recursive_contour_list:
                matched_result_idx.append(idx)
            break
        return matched_result_idx



    #여기가 느려지는 구간이다.
    result_idx = find_chars(possible_contours)




    matched_result = []
    for idx_list in result_idx:
        matched_result.append(np.take(possible_contours, idx_list))



    # visualize possible contours
    temp_result = np.zeros((height, width, channel), dtype=np.uint8)



    number_box=[]


    for r in matched_result:
            for d in r:     
                cv2.rectangle(img_color, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(0, 255, 0))
                number_box.append([d['x'],d['y'],d['w'],d['h']])


    cv2.imwrite("df.jpg",img_color)

    #############################################################################

    # 버블정렬

    for i in range(len(number_box)): 
        for j in range(len(number_box)-(i+1)):
            if number_box[j][0]>number_box[j+1][0]:
                temp=number_box[j]
                number_box[j]=number_box[j+1]
                number_box[j+1]=temp




    number_box_1 = []
    number_box_2 = []
    number_box_3 = []


    valid_plate=[]

    for k in range(len(number_box)):     
        if number_box[k][0]<width*0.33:
            number_box_1.append(number_box[k])
        elif number_box[k][0]<width*0.66:
            number_box_2.append(number_box[k])
        elif number_box[k][0]<width:
            number_box_3.append(number_box[k])



    number_box=[number_box_1,number_box_2,number_box_3]



    select=[]
    for i in range(0,3):
        f_count=0
        for m in range(len(number_box[i])):
            count=0
            for n in range(m+1,(len(number_box[i])-1)):
                delta_x=abs(number_box[i][n+1][0]-number_box[i][m][0])
                if delta_x > 100:
                    break
                delta_y =abs(number_box[i][n+1][1]-number_box[i][m][1])
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
                valid_plate.append(number_box[i][m])
            
                select.append(m)



    valid_plate_temp=[0,0,0]
    cnt=[0,0,0]

    #차량 인식 과정
    for i in range(len(valid_plate)):
        if  valid_plate[i][0]<width*0.33:
            if cnt[0]==0:
                valid_plate_temp[0] = valid_plate[i]
                cnt[0] = 1
        
        elif valid_plate[i][0]<width*0.66:        
            if cnt[1]==0:
                valid_plate_temp[1] = valid_plate[i]
                cnt[1] = 2
        
        elif valid_plate[i][0]<width:
            if cnt[2]==0:
                valid_plate_temp[2] = valid_plate[i]
                cnt[2] = 3

    valid_plate=valid_plate_temp


    number_plate={}


    #번호판 출력과정 
    number_plate = {}

    for i in range(len(cnt)):
        if not (cnt[i] == 0) :    
            number_plate[i+1] =  copy_img [ number_box[i][select[i]][1]-10  :  number_box[i][select[i]][3]+number_box[i][select[i]][1]+10   ,          number_box[i][select[i]][0]-10 :  150+number_box[i][select[i]][0]   ]



    for i in range(len(cnt)):
        if not (cnt[i] == 0) :
            cv2.imshow("show",number_plate[i+1])
            cv2.waitKey(0)

    for i in range(len(cnt)):
        if not (cnt[i] == 0) :
            cv2.imwrite("plate_"+str(cnt[i])+".png",number_plate[i+1])

    return number_plate

