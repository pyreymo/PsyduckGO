import time
import configparser
import os


def get_time():
    """返回当前毫秒时间"""
    return int(time.time() * 1000)


current_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(current_path, "Settings.ini")
conf = configparser.ConfigParser()
conf.read(config_path, encoding='utf-8')

allow_cheat = eval(conf.get("CHEAT", "allow_cheat"))  # 作弊开关，在Settings.txt下直接修改即可

game_state = 0
tutorial = False
time_dict = {'start': get_time()}
spring_chapter = 0
key_list = []
score = 0
win = x, y = 1920, 1080
