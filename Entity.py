from bullet import *


def circle_spawn(x, y, r, n, speed, group_enemy):
    """圆形刷新樱樱怪"""
    for i in range(1, n + 1):
        enemy = Enemy(image_name="enemy/flower.png", radius=25, ai=1, identity="yyg_now_" + str(i),
                      id_0="yyg_start_" + str(i), bullet_speed=speed)
        enemy.rect[0] = x + r * sin(6.28 / n * i)
        enemy.rect[1] = y + r * cos(6.28 / n * i)
        group_enemy.add(enemy)
        common.time_dict[enemy.id] = common.get_time()
        common.time_dict[enemy.id_0] = common.get_time()


def random_spawn(x, y, n, speed, group_enemy):
    """随机刷新篮球"""
    for i in range(1, n + 1):
        enemy = Enemy(image_name="enemy/basketball.png", radius=25, ai=3, identity="bsk_now_" + str(i),
                      id_0="bsk_start_" + str(i), bullet_speed=speed)
        enemy.rect[0] = x + randint(100, 500) * (-1) ** randint(1, 2)
        enemy.rect[1] = y + randint(100, 500) * (-1) ** randint(1, 2)
        group_enemy.add(enemy)
        common.time_dict[enemy.id] = common.get_time()
        common.time_dict[enemy.id_0] = common.get_time()


def cxk_spawn(x, y, group_enemy):
    """生成一只 ❤世界上最好的坤坤 ❤"""
    enemy = Enemy(image_name="enemy/WorldBestKun_big.png", radius=50, ai=2, identity="iKun_now", id_0="iKun_start")
    enemy.rect[0] = x
    enemy.rect[1] = y
    group_enemy.add(enemy)
    common.time_dict["iKun_now"] = common.get_time()
    common.time_dict["iKun_start"] = common.get_time()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_name, radius, ai=0, identity=None, id_0=None, bullet_speed=1.0):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.radius = radius
        self.ai = ai
        self.id = identity
        self.id_0 = id_0
        self.bullet_speed = bullet_speed
        self.lifetime = 0
        self.angle = 0

    def rotate(self, angle):
        self.image = pygame.transform.rotate(pygame.image.load("enemy/basketball.png"), angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, group_bullet, group_enemy, me):
        lifetime = common.time_dict[self.id] - common.time_dict[self.id_0]

        """判断敌人是否出界"""
        if not (common.x * 0.0052 < self.rect[0] < common.x * 0.7708
                and common.y * 0.0093 < self.rect[1] < common.y * 0.9537):
            self.kill()

        """读取ai"""
        if self.ai == 1:
            """1. 樱樱怪：左右横跳，并发射自机狙"""
            self.rect[0] += 5 * sin((lifetime % 1000 / 1000) * 6.28) + 0.61

            if lifetime % 1500 <= 10 and lifetime > 1000:
                shoot_bullet_1(self.rect[0] + 25, self.rect[1] + 25,
                               me.rect[0] + 25, me.rect[1] + 25,
                               self.bullet_speed, group_bullet)

        elif self.ai == 2:
            """2. 世界上做好的坤坤：发射散射弹；发射篮球"""
            self.rect[0] += 1 * sin((lifetime % 1000 / 1000) * 6.28) + 0.61
            if lifetime % 1800 <= 10:
                shoot_bullet_2(self.rect[0] + 50, self.rect[1] + 50, 20, b_group=group_bullet,
                               standard_speed=self.bullet_speed)

        elif self.ai == 3:
            """3. 篮球：风骚走位"""
            self.rect[0] += 3 * cos((lifetime % 1000 / 1000) * 6.28) + 0.61
            self.rect[1] += 3 * sin((lifetime % 1000 / 1000) * 6.28) + 0.61
            self.angle += 5
            self.rotate(self.angle)

        """检测角色与敌人碰撞"""
        if pygame.sprite.collide_circle(me, self):

            if self.ai == 3 and not common.allow_cheat:
                common.game_state = 6  # 判断碰到就死

            if self.id in common.time_dict:
                del common.time_dict[self.id]

            if self.id == "iKun_now":
                pygame.mixer.music.set_volume(max(pygame.mixer.music.get_volume() - 0.3, 0))

            self.kill()

            """分数结算"""
            if self.ai == 1:
                common.score += 1
            elif self.ai == 2:
                common.score += 5

        """刷新敌人的时间"""

        common.time_dict[self.id] = common.get_time()


def redisplay_me(x, y, group_me):
    """绘制带碰撞箱的自己"""
    for old_me in group_me:
        old_me.kill()
    new_me = Me("myself/me_col.png", 10)
    new_me.radius = 10
    new_me.rect[0], new_me.rect[1] = x, y
    group_me.add(new_me)


def restore_me(x, y, group_me):
    """恢复不带碰撞箱的自己"""
    for old_me in group_me:
        old_me.kill()
    new_me = Me("myself/myself4.png", 10)
    new_me.radius = 10
    new_me.rect[0], new_me.rect[1] = x, y
    group_me.add(new_me)


class Me(pygame.sprite.Sprite):
    def __init__(self, image_name, radius):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.radius = radius

    def update(self):
        if common.key_list[pygame.K_LSHIFT]:
            my_speed = 3.0
        else:
            my_speed = 8.0

        if common.key_list[pygame.K_LEFT] and self.rect[0] - my_speed > common.x * 0.0052:
            self.rect[0] -= my_speed
        if common.key_list[pygame.K_RIGHT] and self.rect[0] + my_speed < common.x * 0.7708:
            self.rect[0] += my_speed
        if common.key_list[pygame.K_UP] and self.rect[1] - my_speed > common.y * 0.0093:
            self.rect[1] -= my_speed
        if common.key_list[pygame.K_DOWN] and self.rect[1] + my_speed < common.y * 0.9537:
            self.rect[1] += my_speed

        if common.key_list[pygame.K_LSHIFT]:
            redisplay_me(self.rect[0], self.rect[1], self.groups()[0])
        else:
            restore_me(self.rect[0], self.rect[1], self.groups()[0])
