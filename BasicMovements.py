from djitellopy import tello
from time import sleep # 지연시간

me = tello.Tello()  #me에 tello 넣어주기
me.connect()        # 연결
print(me.get_battery())     # 배터리확인

me.takeoff()    # 비행
# re_control(?, 전진, ?, 회전)
me.send_rc_control(0,50,0,0) # rc 컨트롤러_ 전진 50의 속도로 이동
sleep(3)    # 2초 동안
me.send_rc_control(30,0,0,0) # 오른쪽 방향으로 30 속도로 이동
sleep(1)    # 2초 동안
me.send_rc_control(0,0,0,0) # 전진 후 위치 0으로 재설정 해줘야됨.
me.land()   # 착륙