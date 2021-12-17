from djitellopy import tello
import KeyPressModule as kp
import cv2
import time

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
global img

me.streamon()

def getKeyboardInput():

    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"):ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"):yv = -speed
    elif kp.getKey("d"): yv = speed

    if kp.getKey("e"): me.takeoff()
    if kp.getKey("q"): me.land(); time.sleep(3)

    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)  # imwrite 이미지 저장(저장될 폴더, 파일형식)
        time.sleep(0.3)
    return [lr, fb, ud, yv]

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame     # 프레임 가져와서 나에게 전달
    img = cv2.resize(img, (360, 240))   # 화면 크기
    cv2.imshow("Image", img)    # 이미지 출력
    cv2.waitKey(2)    # 동영상 지연
