import threading
import time
import pygame
from pynput import keyboard

alarm_active = False
alarm_thread = None
timer_thread = None
alarm_ongoing = False
timer_started = False
timer_end_time = None
sound_file = r'sound.mp3' 
timer_time = 55

# pygame 초기화
pygame.mixer.init()

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)  # 반복 재생

def stop_sound():
    pygame.mixer.music.stop()

# 알람을 울리는 함수
def alarm():
    global alarm_ongoing
    alarm_ongoing = True
    play_sound(sound_file)  # 소리 파일을 재생합니다
    while alarm_ongoing:
        time.sleep(1)  # 1초 간격으로 반복
    stop_sound()  # 알람이 꺼졌을 때 소리도 멈춤

# 타이머를 시작하는 함수
def start_timer():
    global alarm_active, timer_started, timer_end_time
    print("58초 타이머 시작")
    timer_started = True
    timer_end_time = time.time() + timer_time
    time.sleep(timer_time)  # timer_time초 대기
    if alarm_active:
        print("알람 시작!")
        start_alarm()

# 알람을 시작하는 함수
def start_alarm():
    global alarm_thread
    if alarm_thread is None or not alarm_thread.is_alive():
        alarm_thread = threading.Thread(target=alarm)
        alarm_thread.start()

# 알람을 멈추는 함수
def stop_alarm():
    global alarm_ongoing
    if alarm_ongoing:
        alarm_ongoing = False
        print("알람이 꺼졌습니다.")
    # 타이머를 새로 시작하도록 준비
    global timer_started
    timer_started = False

def toggle_alarm():
    global alarm_active, alarm_ongoing, timer_thread, timer_started, timer_end_time
    current_time = time.time()

    if timer_started and current_time < timer_end_time:
        # 타이머가 10초가 끝나기 전일 때는 Home 키 입력을 무시
        print("타이머가 끝나기 전에는 알람 설정을 변경할 수 없습니다.")
        return

    if alarm_ongoing:
        # 알람이 울리고 있는 동안 Home 키가 눌렸을 때 알람만 멈추기
        stop_alarm()
        # 타이머를 새로 시작합니다
        timer_thread = threading.Thread(target=start_timer)
        timer_thread.start()
        print("알람이 꺼졌고, 타이머가 다시 시작되었습니다.")
    else:
        if not alarm_active:
            alarm_active = True
            timer_thread = threading.Thread(target=start_timer)
            timer_thread.start()
            print("알람이 설정되었습니다.")
        else:
            print("타이머가 이미 설정되어 있습니다.")
            stop_alarm()
            timer_thread = threading.Thread(target=start_timer)
            timer_thread.start()

# `pynput`을 사용하여 키보드 이벤트 처리
def on_press(key):
    try:
        if key == keyboard.KeyCode.from_czhar('z'):
            toggle_alarm()
    except Exception as e:
        print(f"키 입력 처리 중 에러 발생: {e}")

# Listener를 시작하여 키 입력을 감지합니다
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()