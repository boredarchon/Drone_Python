import cv2
import numpy as np    # 행렬이나 일반적으로 대규모 다차원 배열을 쉽게 처리 할 수 있도록 지원하는 파이썬의 라이브러리
from djitellopy import tello

import time

me = tello.Tello()  #me에 tello 넣어주기
me.connect()        # 연결
print(me.get_battery())     # 배터리확인

me.streamon()   # 비디오 스트림
me.takeoff()
me.send_rc_control(0, 0, 23, 0)
time.sleep(2.2)

w, h = 500, 400    # 360, 240
fbRange = [6200, 6800]# 전진과 후진범위  6200, 6800
pid = [0.4, 0.4, 0]    # 비례, 적분, 미분, PID는 "Process Identification Number", 숫자가 높아지면 회전반경이 커지는거 같음.
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")     # haarcascade_frontalface_default.xml 파일 받아오기, 사람의 얼굴을 구분하기 위해 사람 정면 얼굴에 대해 미리 학습.
    # cv2.CascadeClassifier: Object를 detection하기 위한 라이브러리, 검출기 파일
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # cvtColor: opencv의 컬러이미지 변환, RGB를 BGR로 거꿀로 사용 , COLOR_BGR2GRAY: BGR색상 이미지를 회색조 이미지로 변환
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)    # 입력영상 image에서 다양한 크기의 객체 사각형 영역을 검출
    # detectMultiScale(scaleFactor, minNeighbors)에 이미지를 인자로 지정하면 분류기에 해당하는 검출이 이루어짐.
    # scaleFactor : 각 이미지 스케일에서 이미지 크기가 얼마나 축소되는지 지정하는 매개변수
    # minNeighbors : 각 후보 사각형이 유지해야 하는 이웃 수를 지정하는 매개변수, 값이 높을수록 덜 감지되지만 품질은 높아짐.
    myFaceListC = []    # cx, cy, me 위치
    myFaceListArea = []    # 면적 값


    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x + w, y + h), (0, 0, 255), 2)    # (시작점, 끝점, 색상(0,0,255 : 빨강))
        # rectangle(직사각형)으로 이미지를 보내려면 x,y좌표를 제공해야함, 끝지점(x+w,y+h).(0,0,255)은 색깔, 2는 두깨
        cx = x + w // 2    # 중앙   // : 나누기 연산 후 소수점 이하의 수를 버리고, 정수 부분의 수만 구함.
        cy = y + h // 2    # 중앙
        area = w * h    # 면적은 너비*높이
        cv2.circle(img, (cx,cy), 5, (0,255,0), cv2.FILLED)    # 중앙점
        # cv2.circle(이미지, 원의 중심, 원의 반지름, 색상bgr(0,255,0 : 초록), 선의 타입(FILLED: 안을 채워 넣음)) : 원그리기
        myFaceListC.append([cx,cy])    # append : 리스트에 요소 추가
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:    # 면적에 아무것도 없으면
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]    # cx, cy, area == 0

def trackFace(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w//2    # 이미지의 중심
    speed = pid[0]*error + pid[1]* (error - pError)
    speed = int(np.clip(speed, -100, 100))    # numpy을 활용해 스피드 정의

    if area > fbRange[0] and area < fbRange[1]:    # fbRange[0]보다 크고 fbRange[1]보다 작으면 정지, 녹색영역
        fb = 0
    elif area > fbRange[1]:    # 가까이 있어서 뒤로 물러남.
        fb = -20
    elif area < fbRange[0] and area != 0:    # 멀어서 가까이 다가감.
        fb = 20


    if x == 0:    # 그냥 0이면 모두 0으로 바꿔버림
        speed = 0
        error = 0

    #print(speed, fb)
    me.send_rc_control(0, fb, 0, speed)
    return error


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))       # 창 크기 조절  cv2.resize(이미지 창 이름, 이미지 폭, 이미지 높이)
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)    # trackFace 호출
    cv2.imshow("세얼간이_캡스톤", img)   # 이미지를 모니터에 출력  cv2.imshow(이미지 창 이름, 파일 명)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
