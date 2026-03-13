import threading
import time
import pygame
from pynput import keyboard

알람_활성 = False
알람_스레드 = None
타이머_스레드 = None
알람_울리는중 = False
타이머_시작됨 = False
타이머_종료시간 = None
소리_파일 = r"sound.mp3"
타이머_시간 = 54 # 설치기 알람 시간에 맞춰서 수정하시면 됩니다 기본값 : 55초

# pygame 초기화
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def 소리_재생(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def 소리_정지():
    pygame.mixer.music.stop()

# 알람 실행
def 알람():
    global 알람_울리는중
    알람_울리는중 = True
    소리_재생(소리_파일)

# 알람 시작
def 알람_시작():
    global 알람_스레드
    if 알람_스레드 is None or not 알람_스레드.is_alive():
        알람_스레드 = threading.Thread(target=알람)
        알람_스레드.start()

# 알람 정지
def 알람_정지():
    global 알람_울리는중, 타이머_시작됨
    if 알람_울리는중:
        알람_울리는중 = False
        소리_정지()
    타이머_시작됨 = False

# 타이머 시작
def 타이머_시작():
    global 알람_활성, 타이머_시작됨, 타이머_종료시간
    print(f"{타이머_시간}초 타이머 시작")
    타이머_시작됨 = True
    타이머_종료시간 = time.time() + 타이머_시간
    while time.time() < 타이머_종료시간:
        time.sleep(0.1)
    if 알람_활성:
        print("알람 시작!")
        알람_시작()

# 타이머 실행 스레드
def 타이머_실행():
    global 타이머_스레드
    타이머_스레드 = threading.Thread(target=타이머_시작)
    타이머_스레드.start()

# 알람 토글
def 알람_토글():
    global 알람_활성

    현재_시간 = time.time()

    if 타이머_시작됨 and 현재_시간 < 타이머_종료시간:
        print("타이머가 끝나기 전에는 알람 설정을 변경할 수 없습니다.")
        return

    if 알람_울리는중:
        알람_정지()
        타이머_실행()
        print("알람이 꺼졌고, 타이머가 다시 시작되었습니다.")
    else:
        if not 알람_활성:
            알람_활성 = True
            타이머_실행()
            print("알람이 설정되었습니다.")
        else:
            print("타이머가 이미 설정되어 있습니다.")
            알람_정지()
            타이머_실행()

# 키 입력 감지
def 키_눌림(키):
    try:
        if 키 == keyboard.KeyCode.from_char('z'):
            알람_토글()
    except Exception as e:
        print(f"키 입력 처리 중 에러 발생: {e}")

# 키보드 리스너 실행
with keyboard.Listener(on_press=키_눌림) as listener:
    listener.join()