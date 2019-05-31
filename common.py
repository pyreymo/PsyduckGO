import time


def get_time():
    """返回当前毫秒时间"""
    return int(time.time() * 1000)


game_state = 0
tutorial = False
time_dict = {'start': get_time()}
spring_chapter = 0
key_list = []
score = 0
win = x, y = 1920, 1080
