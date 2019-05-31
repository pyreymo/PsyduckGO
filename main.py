import sys

from pygame.locals import *

from Entity import *
from bullet import *

"""
初始化游戏状态
1 - 开始界面
2 - Spring游戏界面
3，4，5 - 预留关卡
6 - 游戏结束界面
"""

common.game_state = 1
common.spring_chapter = 1

"""初始化窗体"""

pygame.init()
vInfo = pygame.display.Info()
win_size = width, height = vInfo.current_w, vInfo.current_h
common.win = win_size
screen = pygame.display.set_mode(win_size, HWSURFACE | FULLSCREEN, 32)

"""创建计时器"""

clock = pygame.time.Clock()

"""设置窗口图标"""

icon = pygame.image.load("interface/bullet.ico")
pygame.display.set_icon(icon)

"""设置窗口标题"""

pygame.display.set_caption("弹幕游戏")

"""加载背景图片"""
select_bg = pygame.transform.scale(pygame.image.load("interface/season2.png").convert_alpha(), win_size)
spring = pygame.transform.scale(pygame.image.load("interface/spring1.png").convert_alpha(), win_size)
grey_rect = pygame.transform.scale(pygame.image.load("interface/grey_rect.png").convert_alpha(), win_size)

"""加载音频文件"""
pygame.mixer.init()
track = pygame.mixer.music.load('sound/Mirror night.mp3')
pygame.mixer.music.play()

"""初始化时间字典，便于每个敌人储存自己生成的时间"""

common.time_dict = {'start': common.get_time()}

"""向group_me中添加自己"""

my_pos = my_init_x, my_init_y = width // 2 - 300, height - 100
me = Me("myself/myself4.png", radius=10)
me.rect[0], me.rect[1] = my_init_x, my_init_y
group_me = pygame.sprite.Group()
group_me.add(me)

"""初始化敌人序列"""

group_enemy = pygame.sprite.Group()

"""初始化子弹组"""

group_bullet = pygame.sprite.Group()

"""初始化教程"""

tutorial_indicator = 0
tutorial_text = ['你是一只可达鸭。',
                 '为了缓解头痛，你静静漫步在樱花小路上。',
                 '突然，路上出现了几只樱樱怪……',
                 '你决定把它们赶走。',
                 '（友善提醒：人被杀就会死，所以被弹幕撞到就会死。',
                 '没有计时器的关卡只能亲自撞击驱赶敌人，',
                 '有计时器的关卡只用躲过所有弹幕即可获胜。',
                 '操作指导详见侧边栏。）',
                 '那么……躲过旁人的干扰吧。']


def draw_tutorial(text):
    font = pygame.font.Font("font/FZQKBYSJW.ttf", 50)
    my_text = font.render(text, 1, (99, 14, 12))
    grey_rect.blit(my_text, (width * 0.21, height * 0.74))


def state_tutorial():
    """教程"""

    global tutorial_indicator
    global grey_rect
    global spring

    screen.blit(spring, (0, 0))
    spring.blit(grey_rect, (0, 0))
    draw_tutorial(tutorial_text[tutorial_indicator])
    pygame.display.flip()

    """检测鼠标点击"""
    for event in event_list:

        if event.type == MOUSEBUTTONDOWN:
            grey_rect = pygame.image.load("interface/grey_rect.png").convert_alpha()
            spring.blit(grey_rect, (0, 0))
            tutorial_indicator += 1
            try:
                draw_tutorial(tutorial_text[tutorial_indicator])
            except IndexError:
                spring = pygame.image.load("interface/spring1.png").convert_alpha()
                common.tutorial = True
                circle_spawn(me.rect[0], me.rect[1] - height * 0.5556, 300, 10, 4, group_enemy)
                common.spring_chapter = 1
            pygame.display.flip()

    """检测ESC"""
    if common.key_list[K_ESCAPE]:
        sys.exit()

    """检测SPACE"""
    if common.key_list[K_SPACE]:
        grey_rect = pygame.image.load("interface/grey_rect.png").convert_alpha()
        spring.blit(grey_rect, (0, 0))
        tutorial_indicator += 1
        try:
            draw_tutorial(tutorial_text[tutorial_indicator])
        except IndexError:
            spring = pygame.image.load("interface/spring1.png").convert_alpha()
            common.tutorial = True
            circle_spawn(me.rect[0], me.rect[1] - height * 0.5556, 300, 10, 4, group_enemy)
            common.spring_chapter = 1
        pygame.display.flip()

    # common.tutorial = True


def draw_score():
    font = pygame.font.Font("font/euclidb.ttf", 72)
    text = font.render(str(common.score), 1, (60, 19, 9), (234, 222, 211))
    text_rect = text.get_rect(center=(width * 0.9010, height * 0.2315))
    spring.blit(text, text_rect)


def draw_time(time):
    font = pygame.font.Font("font/euclidb.ttf", 65)
    text = font.render('                  ', 1, (60, 19, 9), (234, 222, 211))
    text_rect = text.get_rect(center=(width * 0.9010, height * 0.3935))
    spring.blit(text, text_rect)
    text = font.render(str(time // 1000) + '.' + str(time % 1000 // 100) + ' s / 40.0 s', 1, (60, 19, 9),
                       (234, 222, 211))
    text_rect = text.get_rect(center=(width * 0.9010, height * 0.3935))
    spring.blit(text, text_rect)


win = pygame.image.load("interface/win.png").convert_alpha()
die = pygame.image.load("interface/die.png").convert_alpha()


def stage_6():
    """死亡结算"""

    """绘制结束界面"""
    screen.blit(die, (0, 0))
    pygame.display.flip()

    """检测ESC"""
    if common.key_list[K_r]:
        reset()
    if common.key_list[K_ESCAPE]:
        sys.exit()


def stage_7():
    """胜利结算"""

    """绘制结束界面"""
    screen.blit(win, (0, 0))
    pygame.display.flip()

    """检测ESC"""
    if common.key_list[K_r]:
        reset()
    if common.key_list[K_ESCAPE]:
        sys.exit()


def reset():
    global group_enemy
    global group_bullet
    global group_me
    global track

    """重新玩"""
    if common.spring_chapter != 1:
        pygame.mixer.music.stop()
        track = pygame.mixer.music.load('sound/Mirror night.mp3')
        pygame.mixer.music.play()

    common.score = 0
    start = common.time_dict["start"]
    common.time_dict = {'start': start, "Main": common.get_time()}

    group_enemy = pygame.sprite.Group()
    group_bullet = pygame.sprite.Group()
    group_me = pygame.sprite.Group()

    new_me = Me("myself/myself4.png", radius=10)
    new_me.rect[0], new_me.rect[1] = my_init_x, my_init_y
    group_me.add(new_me)

    common.game_state = 2
    circle_spawn(me.rect[0], me.rect[1] - height * 0.5556, 300, 10, 4, group_enemy)
    common.spring_chapter = 1

    font = pygame.font.Font("font/euclidb.ttf", 72)
    text = font.render('                  ', 1, (60, 19, 9), (234, 222, 211))
    text_rect = text.get_rect(center=(width * 0.9010, height * 0.3935))
    spring.blit(text, text_rect)


def stage_2_insensitive():
    global track
    global group_enemy
    global group_bullet

    if common.spring_chapter == 1:

        if len(group_enemy) == 0:
            """换音乐"""
            pygame.mixer.music.stop()
            track = pygame.mixer.music.load('sound/鸡你太美.mp3')
            pygame.mixer.music.play()

            """从Ch1跳转到Ch2"""
            cxk_spawn(width * 0.10, height * 0.2, group_enemy)
            cxk_spawn(width * 0.62, height * 0.2, group_enemy)
            cxk_spawn(width * 0.10, height * 0.8, group_enemy)
            cxk_spawn(width * 0.62, height * 0.8, group_enemy)
            common.time_dict["Spring_Ch2_start"] = common.get_time()
            common.spring_chapter = 2
            for i in group_me:
                random_spawn(i.rect[0], i.rect[1], 5, group_enemy=group_enemy, speed=1)

    elif common.spring_chapter == 2:

        common.time_dict["Spring_Ch2"] = common.get_time() - common.time_dict["Spring_Ch2_start"]
        draw_time(common.time_dict["Spring_Ch2"])

        if len(group_enemy) == 0 or common.time_dict["Spring_Ch2"] > 40000:
            group_enemy = pygame.sprite.Group()
            group_bullet = pygame.sprite.Group()

            """跳转至Ch3"""
            common.time_dict["Spring_Ch3_start"] = common.get_time()
            common.spring_chapter = 3

            """播放音乐"""
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(1.0)
            track = pygame.mixer.music.load('sound/Next To You.mp3')
            pygame.mixer.music.play()

    elif common.spring_chapter == 3:

        common.time_dict["Spring_Ch3"] = common.get_time() - common.time_dict["Spring_Ch3_start"]
        draw_time(common.time_dict["Spring_Ch3"])

        """循环发射子弹"""
        shoot_bullet_3(3, 2, group_bullet)

        """跳转至Ch4"""
        # TODO 制作新的关卡
        if common.time_dict["Spring_Ch3"] > 40000:
            # common.spring_chapter = 4
            common.game_state = 7


def stage_2_sensitive():
    """时间敏感的刷新项"""

    if common.key_list[K_r]:
        reset()
    if common.key_list[K_ESCAPE]:
        sys.exit()

    """屏幕刷新"""

    screen.fill((200, 200, 200))
    screen.blit(spring, (0, 0))

    for i in group_me:
        group_enemy.update(group_bullet, group_enemy, i)
        group_enemy.draw(screen)

        group_bullet.update(i, group_me, group_enemy, group_bullet)
        group_bullet.draw(screen)

    group_me.update()
    group_me.draw(screen)

    pygame.display.flip()


def stage_1():
    """开场判断"""

    """刷新"""
    screen.fill((200, 200, 200))
    screen.blit(select_bg, (0, 0))
    pygame.display.flip()

    """检测鼠标点击"""
    for event in event_list:

        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if width * 0.5 < mouse_pos[0] < width * 0.75:
                common.game_state = 2
                if common.tutorial:
                    circle_spawn(me.rect[0], me.rect[1] - height * 0.5556, 300, 10, 2.5, group_enemy)

    """检测ESC"""
    if common.key_list[K_ESCAPE]:
        sys.exit()


"""开始游戏"""

common.time_dict["Main"] = common.get_time()

"""主循环"""

while True:
    common.time_dict["Now"] = common.get_time() - common.time_dict["Main"]
    event_list = pygame.event.get()
    common.key_list = pygame.key.get_pressed()

    if common.game_state == 1:
        stage_1()

    elif common.game_state == 2:

        if not common.tutorial:
            state_tutorial()
        else:
            """Spring"""
            if common.time_dict["Now"] % 5 == 1:
                stage_2_insensitive()
                draw_score()
            stage_2_sensitive()

    elif common.game_state == 6:
        stage_6()

    elif common.game_state == 7:
        stage_7()

    clock.tick(120)
