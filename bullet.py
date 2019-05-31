from random import randint

import pygame
from math import sqrt, sin, cos, atan2

import common


def get_angle(x, y):
    a = atan2(y, x)
    ret = a * 180 / 3.1415926
    if ret > 360:
        ret -= 360
    if ret < 0:
        ret += 360
    return ret


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_name, radius, angle=0, ai=0, aim_x=0, aim_y=0, speed=1.0):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.radius = radius
        self.angle = angle
        self.aim_x = aim_x
        self.aim_y = aim_y
        self.ai = ai
        self.speed = speed
        self.speed_x = 0
        self.speed_y = 0
        self.r = 50  # 散射半径
        self.id = 0  # 散射下标

    def update(self, me, group_me, group_enemy, group_bullet):

        if not -500 < self.rect[0] < 1510 or not -600 < self.rect[1] < 1600:
            self.kill()

        if pygame.sprite.collide_circle(me, self) and not common.allow_cheat:
            print("\nYou lost.")
            group_me.remove()
            group_enemy.remove()
            group_bullet.remove()
            common.game_state = 6  # 判断碰到就死

        if self.ai == 1:
            """1. 自机狙"""
            self.rect[0] += self.speed_x
            self.rect[1] += self.speed_y
            self.rotate(get_angle(self.speed_x, self.speed_y))

        elif self.ai == 2:
            """2. 散射弹"""
            num = 20
            self.r += self.speed
            d = 6.28 * ((common.time_dict["iKun_now"] - common.time_dict["iKun_start"]) % 1000 / 1000) / 20
            self.rect[0] = self.aim_x + self.r * sin(6.28 / num * self.id + d)
            self.rect[1] = self.aim_y + self.r * cos(6.28 / num * self.id + d)

        elif self.ai == 3:
            """3. 随缘弹"""
            self.rect[1] += self.speed
            # self.rotate(self.angle)  # 性能不允许

    def rotate(self, angle):
        self.image = pygame.transform.rotate(pygame.image.load("bullet/bullet3.png"), angle)
        self.rect = self.image.get_rect(center=self.rect.center)


def shoot_bullet_1(x: int, y: int, aim_x: int, aim_y: int, standard_speed: float, b_group: pygame.sprite.Group):
    """自机狙"""
    b = Bullet("bullet/bullet3.png", radius=5, aim_x=aim_x, aim_y=aim_y, speed=standard_speed, ai=1)
    b.rect[0], b.rect[1] = x, y
    b_group.add(b)
    nx = b.aim_x - b.rect[0] - 7
    ny = b.aim_y - b.rect[1] - 7
    nd = sqrt(nx ** 2 + ny ** 2)
    b.speed_x = nx / nd * b.speed
    b.speed_y = ny / nd * b.speed


def shoot_bullet_2(x: int, y: int, num: int, standard_speed: float, b_group: pygame.sprite.Group):
    """散射弹"""
    for i in range(1, num + 1):
        b = Bullet("bullet/note.png", radius=5, speed=standard_speed,
                   aim_x=x, aim_y=y, ai=2)
        b.r = 50
        b.id = i
        b.rect[0] = x + b.r * sin(6.28 / num * (i - 1))
        b.rect[1] = y + b.r * cos(6.28 / num * (i - 1))
        b_group.add(b)


def shoot_bullet_3(num: int, standard_speed: float, b_group: pygame.sprite.Group):
    """顶部随机发射"""
    for i in range(1, num + 1):
        b = Bullet("bullet/bullet3.png", radius=5, speed=standard_speed, ai=3)
        b.angle = randint(0, 180)
        b.rect[0] = randint(15, 1500)
        b.rect[1] = 0
        b_group.add(b)
