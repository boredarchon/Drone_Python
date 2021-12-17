import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))    # pygame 설정모듈, 사이즈

def getKey(keyName):

    ans = False     # 반환값은 기본적으로 False
    for eve in pygame.event.get(): pass     # for문을 사용한 pygame 이벤트
    keyInput = pygame.key.get_pressed()     # keyInput에 pygame에 press되는 값들 넣어주기
    myKey = getattr(pygame, 'K_{}'.format(keyName))     # getattr(object, 'name'): object라는 오브젝트 내부의 name이라는 멤버를 반환.
    print('K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()     # pygame의 display에 update
    return ans

def main():
    if getKey("LEFT"):
        print("Left key pressed")
    if getKey("RIGHT"):
        print("Right key Pressed")

if __name__ == '__main__':    # __name__이라는 변수의 값이 __main__이라면 아래의 코드를 실행하라.
    init()
    while True:
        main()