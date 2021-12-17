from djitellopy import tello
import cv2  # 영상처리하는 라이브러리 opencv

me = tello.Tello()  #me에 tello 넣어주기
me.connect()        # 연결
print(me.get_battery())     # 배터리확인

me.streamon()   # 비디오 스트림

while True:
    img = me.get_frame_read().frame     # 프레임 가져와서 나에게 전달
    img = cv2.resize(img, (360, 240))   # 화면 크기
    cv2.imshow("Image", img)    # 이미지 출력
    cv2.waitKey(2)    # 동영상 지연