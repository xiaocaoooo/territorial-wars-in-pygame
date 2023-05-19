# 导入所需的模块
import sys
import pygame
import math
import random
import time
# import keyboard


# 20x

open("./start.txt", "w").close()
open("./end.txt", "w").close()

# 使用pygame之前必须初始化
pygame.init()

SPEED = 20

start_time = time.time()

COLOR = ["up", "red", "yellow", "lime", "blue"]
COLOR_LIST = [(128, 128, 128), (255, 0, 0),
              (255, 255, 0), (0, 255, 0), (0, 0, 255)]
COLOR_LIST_2 = [(64, 64, 64), (128, 0, 0),
                (128, 128, 0), (0, 128, 0), (0, 0, 128)]
BLOCK_WIDTH = 4
RADIUS = 10
TEXT_SIZE = 50

WIDTH, HEIGHT = (1920, 1080)

MAX_BULLET = 2**5+8
START_BULLET = 2**10
START_BULLET_TEMP = 2**5
BULLET_LIFE = 3
BULLET_VEL = 3
BULLET_LUNCH_VEL = 32
UP_START_NUM = 1
# UP_GENERATE_TIME = 0.1*SPEED
UP_GENERATE_TIME = 0.0

PEN_FADE_TIME = 3 * SPEED

BALL_NUM = 4

# state = False

fps = 0
t_time = time.time()
t2_time = time.time()

red_state = 1
yellow_state = 1
lime_state = 1
blue_state = 1

red_bullet = START_BULLET*1
yellow_bullet = START_BULLET*1
lime_bullet = START_BULLET*1
blue_bullet = START_BULLET*1

red_bullet_temp = START_BULLET_TEMP
yellow_bullet_temp = START_BULLET_TEMP
lime_bullet_temp = START_BULLET_TEMP
blue_bullet_temp = START_BULLET_TEMP

rand = random.random()


# font = pygame.font.Font(
#     ["\\".join(__file__.split("\\")[:-1])+'FiraCode-Bold.ttf'], BLOCK_WIDTH*5)
font = pygame.font.Font(None, TEXT_SIZE)

# GRAVITY = [0, 0.3]


def collide(item1, item2):
    x = abs(item1.x-item2.x)
    y = abs(item1.y-item2.y)
    distance = math.sqrt(x**2+y**2)
    return distance < BLOCK_WIDTH*1.0


def getDistance(x1, y1, x2, y2):
    x = abs(x1-x2)
    y = abs(y1-y2)
    return math.sqrt(x**2+y**2)


def randomVel(n=1):
    # 0-2pi range, 0 degrees is at the top of the screen.
    angle = random.random()*360
    # angle = 45
    # angle = (time.time()*360+(random.random()*10-5))%360
    # degrees to radians.  0 degrees is at the top of the screen.  0.0 degrees is at the top
    angle *= 0.25*math.pi
    return [math.sin(angle)*n, math.cos(angle)*n]


def randomVel2(n=1):
    # 0-2pi range, 0 degrees is at the top of the screen.
    # angle = math.radians(random.random()*360)
    angle = ((time.time()-start_time)*360/SPEED*0.25 + rand*360) % 360
    # angle = (((int((time.time()-start_time)/SPEED*2+rand*2**32)%8)+(random.random()*2-1)*0.25)*45)
    # print(angle)
    # degrees to radians.  0 degrees is at the top of the screen.  0.0 degrees is at the top
    angle *= math.pi/360*2
    return [math.sin(angle)*n, math.cos(angle)*n]


class Block:
    def __init__(self, x: int, y: int, color: int | str, screen, alpha: int) -> None:
        self.x = x
        self.y = y
        self.alpha = alpha
        if type(color) == int:
            self.color = color
        elif type(color) == str:
            self.color = COLOR.index(color)
        self.draw(screen)

    def draw(self, screen) -> None:
        # if self.color == 0:
        #     pygame.draw.rect(screen, (128, 128, 128), (self.x, self.y, WIDTH, WIDTH))
        # elif self.color == 1:
        #     pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, WIDTH, WIDTH))
        # elif self.color == 2:
        #     pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, WIDTH, WIDTH))
        # elif self.color == 3:
        #     pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, WIDTH, WIDTH))
        # elif self.color == 4:
        #     pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, WIDTH, WIDTH))
        self.main = pygame.draw.rect(
            screen, COLOR_LIST[self.color], (self.x, self.y, BLOCK_WIDTH, BLOCK_WIDTH))
        # s = pygame.Surface((BLOCK_WIDTH, BLOCK_WIDTH))		# the size of your rect
        # s.set_alpha(self.alpha)										# alpha level
        # s.fill(COLOR_LIST[self.color])						# this fills the entire surface
        # # (0,0) are the top-left coordinates
        # screen.blit(s, (self.x, self.y))


class Ball:
    def __init__(self, x, y, color: int | str, screen) -> None:
        self.start_x = x
        self.start_y = y
        self.x = x(None)
        self.y = y(None)
        self.radius = RADIUS
        if type(color) == int:
            self.color = color
        elif type(color) == str:
            self.color = COLOR.index(color)
        # self.vel = [(random.random()*2-1)*10, (random.random()*1-1)*15]
        self.vel = randomVel(10)
        # print(self.vel[1])
        self.draw(screen)

    def draw(self, screen) -> None:
        self.main = pygame.draw.circle(
            screen, COLOR_LIST[self.color], (self.x, self.y), self.radius)

    def update(self, screen) -> None:
        global red_bullet, yellow_bullet, lime_bullet, blue_bullet, red_bullet_temp, yellow_bullet_temp, lime_bullet_temp, blue_bullet_temp
        self.x += self.vel[0]*1
        self.y += self.vel[1]*1
        self.vel[0] = self.vel[0]*0.99
        self.vel[1] = self.vel[1]*0.9+(abs(self.vel[1]*0.9)*0.1)+0.05
        if ((self.color in [1, 3] and (self.x < self.radius or self.x > (WIDTH-HEIGHT)//2-self.radius-2)) or
                (self.color in [2, 4] and (self.x > WIDTH-(self.radius) or self.x < WIDTH-((WIDTH-HEIGHT)//2-self.radius-2)))):
            self.vel[0] = -self.vel[0]

            # if self.color in [1, 3]:
            #     if self.x < self.radius:
            #         self.x = (WIDTH-HEIGHT)//2-self.radius-2
            #     elif self.x > (WIDTH-HEIGHT)//2-self.radius-2:
            #         self.x = self.radius
            # elif self.color in [2, 4]:
            #     if self.x > WIDTH-(self.radius):
            #         self.x = WIDTH-((WIDTH-HEIGHT)//2-self.radius-2)
            #     elif self.x < WIDTH-((WIDTH-HEIGHT)//2-self.radius-2):
            #         self.x = WIDTH-(self.radius)

        if self.y > HEIGHT:
            if self.color == 1:
                red_bullet_temp *= 2
            elif self.color == 2:
                yellow_bullet_temp *= 2
            elif self.color == 3:
                lime_bullet_temp *= 2
            elif self.color == 4:
                blue_bullet_temp *= 2
            # if 0 < self.x < (WIDTH-HEIGHT)//2*0.75 or WIDTH-(WIDTH-HEIGHT)//2*0.75 < self.x < WIDTH:
            #     if self.color == 1:
            #         red_bullet_temp *= 2
            #     elif self.color == 2:
            #         yellow_bullet_temp *= 2
            #     elif self.color == 3:
            #         lime_bullet_temp *= 2
            #     elif self.color == 4:
            #         blue_bullet_temp *= 2
            # elif (WIDTH-HEIGHT)//2*0.75 < self.x < (WIDTH-HEIGHT)//2*1 or WIDTH-(WIDTH-HEIGHT)//2*1 < self.x < WIDTH-(WIDTH-HEIGHT)//2*0.75:
            #     if self.color == 1:
            #         red_bullet += red_bullet_temp
            #         red_bullet_temp = START_BULLET_TEMP
            #     elif self.color == 2:
            #         yellow_bullet += yellow_bullet_temp
            #         yellow_bullet_temp = START_BULLET_TEMP
            #     elif self.color == 3:
            #         lime_bullet += lime_bullet_temp
            #         lime_bullet_temp = START_BULLET_TEMP
            #     elif self.color == 4:
            #         blue_bullet += blue_bullet_temp
            #         blue_bullet_temp = START_BULLET_TEMP

            self.x = self.start_x
            self.y = self.start_y
            self.__init__(self.x, self.y, self.color, screen)


class Bullet:
    def __init__(self, x: int, y: int, color: int | str, vel: list, screen, life: int) -> None:
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.life = life
        if type(color) == int:
            self.color = color
        elif type(color) == str:
            self.color = COLOR.index(color)
        self.vel = randomVel()
        # self.vel = [(WIDTH//2-x)/(WIDTH//2-x)-2,(HEIGHT//2-y)//(HEIGHT//2-y)+0.25] #TODO
        self.draw(screen)

    def draw(self, screen) -> None:
        self.main = pygame.draw.circle(
            screen, COLOR_LIST_2[self.color], (int(self.x), int(self.y)), BLOCK_WIDTH*0.5)

    def reset(self, screen) -> None:
        self.x = self.start_x
        self.y = self.start_y
        # if self.color == 1:
        #     self.vel = [random.random()-0.1, random.random()-0.1]
        # elif self.color == 2:
        #     self.vel = [random.random()-0.9, random.random()-0.1]
        # elif self.color == 3:
        #     self.vel = [random.random()-0.1, random.random()-0.9]
        # elif self.color == 4:
        #     self.vel = [random.random()-0.9, random.random()-0.9]
        self.vel = randomVel()
        self.__init__(self.x, self.y, self.color, self.vel, screen, self.life)

    def update(self, block_list: list[list[Block]], idx: int, screen) -> None:
        global bullet_list
        self.x += self.vel[0]*BULLET_VEL
        self.y += self.vel[1]*BULLET_VEL
        if self.x < BLOCK_WIDTH*0.5*0.5+(WIDTH-HEIGHT)//2:
            self.vel[0] = (abs(self.vel[0]))
            # bullet_list.remove((bullet_list[idx]))
            # self.reset(screen)
            return None
        elif self.x > WIDTH-BLOCK_WIDTH*0.5*0.5-(WIDTH-HEIGHT)//2:
            self.vel[0] = -(abs(self.vel[0]))
            # bullet_list.remove((bullet_list[idx]))
            # self.reset(screen)
            return None
        if self.y < 0:
            self.vel[1] = (abs(self.vel[1]))
            # bullet_list.remove((bullet_list[idx]))
            # self.reset(screen)
            return None
        elif self.y > HEIGHT:
            self.vel[1] = -(abs(self.vel[1]))
            # bullet_list.remove((bullet_list[idx]))
            # self.reset(screen)
            return None
        # print(self.x, self.y)
        # for y in block_list:
        #     for b in y:
        #         if collide(self, b) and b.color != self.color:
        #             b.color = self.color
        #             bullet_list.remove((bullet_list[idx]))
        #             return None
        y = int((self.y)//BLOCK_WIDTH)
        x = int((self.x-(WIDTH-HEIGHT)//2)//BLOCK_WIDTH)
        # if collide(self, block_list[y][x]) and b.color != self.color:
        try:
            if block_list[y][x].color != self.color:
                block_list[y][x].color = self.color
                self.life -= 1
                # block_list[y-1][x-1].color = self.color
                # block_list[y-1][x].color = self.color
                # block_list[y-1][x+1].color = self.color
                # block_list[y][x-1].color = self.color
                # block_list[y][x+1].color = self.color
                # block_list[y+1][x-1].color = self.color
                # block_list[y+1][x].color = self.color
                # block_list[y+1][x+1].color = self.color
                # bullet_list.remove((bullet_list[idx]))
                # return None
            # TODO
        except:
            if self.x < BLOCK_WIDTH*0.5*0.5+(WIDTH-HEIGHT)//2:
                self.vel[0] = (abs(self.vel[0]))
                # bullet_list.remove((bullet_list[idx]))
                # self.reset(screen)
                return None
            elif self.x > WIDTH-BLOCK_WIDTH*0.5*0.5-(WIDTH-HEIGHT)//2:
                self.vel[0] = -(abs(self.vel[0]))
                # bullet_list.remove((bullet_list[idx]))
                # self.reset(screen)
                return None
            if self.y < 0:
                self.vel[1] = (abs(self.vel[1]))
                # bullet_list.remove((bullet_list[idx]))
                # self.reset(screen)
                return None
            elif self.y > HEIGHT:
                self.vel[1] = -(abs(self.vel[1]))
                # bullet_list.remove((bullet_list[idx]))
                # self.reset(screen)
            return None
        if not self.life:
            bullet_list.remove((bullet_list[idx]))
            return None


class Pen:
    def __init__(self, x: int, y: int, color: int, fade_time: int, radius: int):
        self.x = x
        self.y = y
        if type(color) == int:
            self.color = color
        elif type(color) == str:
            self.color = COLOR.index(color)
        self.fade_time = fade_time
        self.radius = radius
        self.time = time.time()

    def draw(self, screen):
        c = []
        for i in COLOR_LIST[self.color]:
            # print(i)
            t = (int(i*((1-((time.time()-self.time)*2)/self.fade_time)*1+0)))
            if t < 0:
                t = 0
            c.append(t)

        pygame.draw.circle(
            screen, c, (self.x, self.y), self.radius*(1-(time.time()-self.time)/self.fade_time))

    def update(self, idx: int):
        global pen_list
        if (time.time()-self.time) > self.fade_time:
            pen_list.remove(pen_list[idx])


class Up:
    def __init__(self, x: int, y: int):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.color = 0
        self.vel = randomVel2(BULLET_VEL*0.05)
        self.image = pygame.transform.rotate(
            pygame.image.load('up50_2.png').convert_alpha(), 0)

    def draw(self, screen):
        screen.blit(self.image, (self.x-25, self.y-25))

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vel = randomVel2(BULLET_VEL*0.05)

    def update(self, block_list: list[list[Block]], idx: int):
        global up_list
        self.x += self.vel[0]
        self.y += self.vel[1]
        if BLOCK_WIDTH*0.5*0.5+(WIDTH-HEIGHT)//2 > self.x:
            # self.vel[1] = (abs(self.vel[1]))
            # bullet_list.remove((bullet_list[idx]))
            self.reset()
            return None
        elif self.x > WIDTH-BLOCK_WIDTH*0.5*0.5-(WIDTH-HEIGHT)//2:
            # self.vel[1] = (-abs(self.vel[1]))
            # bullet_list.remove((bullet_list[idx]))
            self.reset()
            return None
        if BLOCK_WIDTH*0.5*0.5 > self.y:
            # self.vel[0] = (-abs(self.vel[0]))
            # bullet_list.remove((bullet_list[idx]))
            self.reset()
            return None
        elif self.y > WIDTH-BLOCK_WIDTH*0.5*0.5:
            # self.vel[0] = (abs(self.vel[0]))
            # bullet_list.remove((bullet_list[idx]))
            self.reset()
            return None
        y = int((self.y)//BLOCK_WIDTH)
        x = int((self.x-(WIDTH-HEIGHT)//2)//BLOCK_WIDTH)
        try:
            if block_list[y][x].color != self.color:
                block_list[y][x].color = self.color
                up_list.remove((up_list[idx]))
                # self.life -= 1
                # bullet_list.remove((bullet_list[idx]))
                # return None
        except:
            self.reset()


def update():
    global MAX_BULLET, red_bullet_text, yellow_bullet_text, lime_bullet_text, blue_bullet_text, red_stateyellow_state, lime_state, blue_state, red_bullet, red_bullet_temp, yellow_bullet, yellow_bullet_temp, lime_bullet, lime_bullet_temp, blue_bullet, blue_bullet_temp, fps, t_time, fps_text, red_state, yellow_state, lime_state, blue_state, t2_time
    # 循环获取事件，监听事件状态
    for event in pygame.event.get():
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            # 卸载所有模块
            pygame.quit()
            # 终止程序，确保退出程序
            sys.exit()

    # 清除屏幕
    screen.fill((0, 0, 0))
    # pygame.draw.rect(screen, (255, 255, 255, 127), pygame.Rect(0, 0, 1000, 750))
    # s = pygame.Surface((WIDTH, HEIGHT))		# the size of your rect
    # s.set_alpha(16)							# alpha level
    # s.fill((0, 0, 0))						# this fills the entire surface
    # screen.blit(s, (0, 0))					# (0,0) are the top-left coordinates

    # s = pygame.Surface((HEIGHT, HEIGHT))		# the size of your rect
    # s.set_alpha(64)								# alpha level
    # s.fill((0,0,0))								# this fills the entire surface
    # # (0,0) are the top-left coordinates
    # screen.blit(s, ((WIDTH-HEIGHT)//2, 0))

    # Draw Pen
    for p in pen_list:
        p.update(pen_list.index(p))
        p.draw(screen)

    # ball
    for b in ball_list:
        b.update(screen)
        b.draw(screen)
        pen_list.append(Pen(b.x, b.y, b.color, PEN_FADE_TIME, b.radius))

    # red_bullet_text = font.render(
    #     str(red_bullet if red_bullet > 0 else red_bullet_temp), True, (255, 0, 0))
    # yellow_bullet_text = font.render(
    #     str(yellow_bullet if yellow_bullet > 0 else yellow_bullet_temp), True, (255, 255, 0))
    # lime_bullet_text = font.render(
    #     str(lime_bullet if lime_bullet > 0 else lime_bullet_temp), True, (0, 255, 0))
    # blue_bullet_text = font.render(
    #     str(blue_bullet if blue_bullet > 0 else blue_bullet_temp), True, (0, 0, 255))
    red_bullet_text = font.render(
        (" %i " if red_bullet > 0 else "(%i)") % (red_bullet if red_bullet > 0 else red_bullet_temp), True, (255, 0, 0))
    yellow_bullet_text = font.render(
        (" %i " if yellow_bullet > 0 else "(%i)") % (yellow_bullet if yellow_bullet > 0 else yellow_bullet_temp), True, (255, 255, 0))
    lime_bullet_text = font.render(
        (" %i " if lime_bullet > 0 else "(%i)") % (lime_bullet if lime_bullet > 0 else lime_bullet_temp), True, (0, 255, 0))
    blue_bullet_text = font.render(
        (" %i " if blue_bullet > 0 else "(%i)") % (blue_bullet if blue_bullet > 0 else blue_bullet_temp), True, (0, 0, 255))
    screen.blit(red_bullet_text, (TEXT_SIZE*0.5, (10*1+TEXT_SIZE*1)))
    screen.blit(yellow_bullet_text, (TEXT_SIZE*0.5, (10*2+TEXT_SIZE*2)))
    screen.blit(lime_bullet_text, (TEXT_SIZE*0.5, (10*3+TEXT_SIZE*3)))
    screen.blit(blue_bullet_text, (TEXT_SIZE*0.5, (10*4+TEXT_SIZE*4)))

    max_bullet_text = font.render(
        "Max: %i" % (MAX_BULLET), True, (255, 255, 255))
    screen.blit(max_bullet_text, (TEXT_SIZE*0.5, (10*5+TEXT_SIZE*5)))

    # block
    # n = 0
    for x in blocks_list:
        for b in x:
            b.draw(screen)
            # print(n)
            # n += 1

    # state
    if red_state and blocks_list[0][0].color != 1:
        red_state = 0
    if yellow_state and blocks_list[0][-1].color != 2:
        yellow_state = 0
    if lime_state and blocks_list[-1][0].color != 3:
        lime_state = 0
    if blue_state and blocks_list[-1][-1].color != 4:
        blue_state = 0

    # 显示方框
    pygame.draw.rect(screen, (0, 255, 0),
                     (0, HEIGHT-50, (WIDTH-HEIGHT)//2, 50))
    pygame.draw.rect(screen, (0, 255, 0),
                     (WIDTH-(WIDTH-HEIGHT)//2, HEIGHT-50, WIDTH-(WIDTH-HEIGHT)//2, 50))
    # pygame.draw.rect(screen, (255, 0, 0),
    #                  ((WIDTH-HEIGHT)//2*0.75, HEIGHT-50, (WIDTH-HEIGHT)//2*0.25, 50))
    # pygame.draw.rect(screen, (255, 0, 0),
    #                  (WIDTH-(WIDTH-HEIGHT)//2, HEIGHT-50, (WIDTH-HEIGHT)//2*0.25, 50))

    # 显示炮台 (圆形)
    if red_state:
        pygame.draw.circle(screen, COLOR_LIST_2[1], (
            blocks_list[0][0].x+BLOCK_WIDTH*2, blocks_list[0][0].y+BLOCK_WIDTH*2), BLOCK_WIDTH*2)
    if yellow_state:
        pygame.draw.circle(screen, COLOR_LIST_2[2], (
            blocks_list[0][-1].x-BLOCK_WIDTH*1, blocks_list[0][-1].y+BLOCK_WIDTH*2), BLOCK_WIDTH*2)
    if lime_state:
        pygame.draw.circle(screen, COLOR_LIST_2[3], (
            blocks_list[-1][0].x+BLOCK_WIDTH*2, blocks_list[-1][0].y-BLOCK_WIDTH*1), BLOCK_WIDTH*2)
    if blue_state:
        pygame.draw.circle(screen, COLOR_LIST_2[4], (
            blocks_list[-1][-1].x-BLOCK_WIDTH*1, blocks_list[-1][-1].y-BLOCK_WIDTH*1), BLOCK_WIDTH*2)

    # t.update(blocks_list)
    # t.draw(screen)
    for b in bullet_list:
        b.update(blocks_list, bullet_list.index(b), screen)
        b.draw(screen)

    if time.time()-t2_time > UP_GENERATE_TIME:
        t2_time = time.time()        # 记得将这个变量置为0。如果不能在0.5秒内完成任务
        up_list.append(Up(WIDTH//2, HEIGHT//2))

    try:
        # Updating the position of the blocks on the screen. 将 block 的位置更新到屏幕上。
        for up in range(len(up_list)):
            up_list[up].update(blocks_list, up)
            up_list[up].draw(screen)
    except IndexError:
        pass

    if red_bullet_temp >= MAX_BULLET:
        red_bullet = MAX_BULLET
        red_bullet_temp = START_BULLET_TEMP
        MAX_BULLET = int(MAX_BULLET*1.05)
    if yellow_bullet_temp >= MAX_BULLET:
        yellow_bullet = MAX_BULLET
        yellow_bullet_temp = START_BULLET_TEMP
        MAX_BULLET = int(MAX_BULLET*1.05)
    if lime_bullet_temp >= MAX_BULLET:
        lime_bullet = MAX_BULLET
        lime_bullet_temp = START_BULLET_TEMP
        MAX_BULLET = int(MAX_BULLET*1.05)
    if blue_bullet_temp >= MAX_BULLET:
        blue_bullet = MAX_BULLET
        blue_bullet_temp = START_BULLET_TEMP
        MAX_BULLET = int(MAX_BULLET*1.05)

    # if red_state and red_bullet > 0:
    #     red_bullet -= 1
    #     bullet_list.append(Bullet(
    #         blocks_list[0][0].x+BLOCK_WIDTH*1, blocks_list[0][0].y+BLOCK_WIDTH*1, 1, [random.random()-0.1, random.random()-0.1], screen, BULLET_LIFE))
    # if yellow_state and yellow_bullet > 0:
    #     yellow_bullet -= 1
    #     bullet_list.append(Bullet(
    #         blocks_list[0][-1].x-BLOCK_WIDTH*0, blocks_list[0][-1].y+BLOCK_WIDTH*1, 2, [random.random()-0.9, random.random()-0.1], screen, BULLET_LIFE))
    # if lime_state and lime_bullet > 0:
    #     lime_bullet -= 1
    #     bullet_list.append(Bullet(
    #         # blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, -1], screen))
    #         blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, random.random()-0.9], screen, BULLET_LIFE))
    # if blue_state and blue_bullet > 0:
    #     blue_bullet -= 1
    #     bullet_list.append(Bullet(
    #         blocks_list[-1][-1].x-BLOCK_WIDTH*0, blocks_list[-1][-1].y-BLOCK_WIDTH*0, 4, [random.random()-0.9, random.random()-0.9], screen, BULLET_LIFE))
    # --- #
    # if red_state and red_bullet > 0:
    #     red_bullet -= math.ceil(red_bullet/2)
    #     for _ in range(math.ceil(red_bullet/2)):
    #         bullet_list.append(Bullet(
    #             blocks_list[0][0].x+BLOCK_WIDTH*1, blocks_list[0][0].y+BLOCK_WIDTH*1, 1, [random.random()-0.1, random.random()-0.1], screen, BULLET_LIFE))
    # if yellow_state and yellow_bullet > 0:
    #     yellow_bullet -= math.ceil(yellow_bullet/2)
    #     for _ in range(math.ceil(yellow_bullet/2)):
    #         bullet_list.append(Bullet(
    #             blocks_list[0][-1].x-BLOCK_WIDTH*0, blocks_list[0][-1].y+BLOCK_WIDTH*1, 2, [random.random()-0.9, random.random()-0.1], screen, BULLET_LIFE))
    # if lime_state and lime_bullet > 0:
    #     lime_bullet -= math.ceil(lime_bullet/2)
    #     for _ in range(math.ceil(lime_bullet/2)):
    #         bullet_list.append(Bullet(
    #             # blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, -1], screen))
    #             blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, random.random()-0.9], screen, BULLET_LIFE))
    # if blue_state and blue_bullet > 0:
    #     blue_bullet -= math.ceil(blue_bullet/2)
    #     for _ in range(math.ceil(blue_bullet/2)):
    #         bullet_list.append(Bullet(
    #             blocks_list[-1][-1].x-BLOCK_WIDTH*0, blocks_list[-1][-1].y-BLOCK_WIDTH*0, 4, [random.random()-0.9, random.random()-0.9], screen, BULLET_LIFE))
    # --- #
    # if red_state and red_bullet > 0:
    #     red_bullet -= len(str(red_bullet))*2**2
    #     for _ in range(len(str(red_bullet))*2**2):
    #         bullet_list.append(Bullet(
    #             blocks_list[0][0].x+BLOCK_WIDTH*1, blocks_list[0][0].y+BLOCK_WIDTH*1, 1, [random.random()-0.1, random.random()-0.1], screen, BULLET_LIFE))
    # if yellow_state and yellow_bullet > 0:
    #     yellow_bullet -= len(str(yellow_bullet))*2**2
    #     for _ in range(len(str(yellow_bullet))*2**2):
    #         bullet_list.append(Bullet(
    #             blocks_list[0][-1].x-BLOCK_WIDTH*0, blocks_list[0][-1].y+BLOCK_WIDTH*1, 2, [random.random()-0.9, random.random()-0.1], screen, BULLET_LIFE))
    # if lime_state and lime_bullet > 0:
    #     lime_bullet -= len(str(lime_bullet))*2**2
    #     for _ in range(len(str(lime_bullet))*2**2):
    #         bullet_list.append(Bullet(
    #             # blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, -1], screen))
    #             blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, random.random()-0.9], screen, BULLET_LIFE))
    # if blue_state and blue_bullet > 0:
    #     blue_bullet -= len(str(blue_bullet))*2**2
    #     for _ in range(len(str(blue_bullet))*2**2):
    #         bullet_list.append(Bullet(
    #             blocks_list[-1][-1].x-BLOCK_WIDTH*0, blocks_list[-1][-1].y-BLOCK_WIDTH*0, 4, [random.random()-0.9, random.random()-0.9], screen, BULLET_LIFE))
    # --- #
    if red_state and red_bullet > 0:
        red_bullet -= BULLET_LUNCH_VEL
        for _ in range(BULLET_LUNCH_VEL):
            bullet_list.append(Bullet(
                blocks_list[0][0].x+BLOCK_WIDTH*1, blocks_list[0][0].y+BLOCK_WIDTH*1, 1, [random.random()-0.1, random.random()-0.1], screen, BULLET_LIFE))
    if yellow_state and yellow_bullet > 0:
        yellow_bullet -= BULLET_LUNCH_VEL
        for _ in range(BULLET_LUNCH_VEL):
            bullet_list.append(Bullet(
                blocks_list[0][-1].x-BLOCK_WIDTH*0, blocks_list[0][-1].y+BLOCK_WIDTH*1, 2, [random.random()-0.9, random.random()-0.1], screen, BULLET_LIFE))
    if lime_state and lime_bullet > 0:
        lime_bullet -= BULLET_LUNCH_VEL
        for _ in range(BULLET_LUNCH_VEL):
            bullet_list.append(Bullet(
                # blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, -1], screen))
                blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, random.random()-0.9], screen, BULLET_LIFE))
    if blue_state and blue_bullet > 0:
        blue_bullet -= BULLET_LUNCH_VEL
        for _ in range(BULLET_LUNCH_VEL):
            bullet_list.append(Bullet(
                blocks_list[-1][-1].x-BLOCK_WIDTH*0, blocks_list[-1][-1].y-BLOCK_WIDTH*0, 4, [random.random()-0.9, random.random()-0.9], screen, BULLET_LIFE))
    # --- #
    # if red_state and red_bullet > 0:
    #     bullet_list.append(Bullet(
    #         blocks_list[0][0].x+BLOCK_WIDTH*1, blocks_list[0][0].y+BLOCK_WIDTH*1, 1, [random.random()-0.1, random.random()-0.1], screen, red_bullet))
    #     red_bullet = 0
    # if yellow_state and yellow_bullet > 0:
    #     bullet_list.append(Bullet(
    #         blocks_list[0][-1].x-BLOCK_WIDTH*0, blocks_list[0][-1].y+BLOCK_WIDTH*1, 2, [random.random()-0.9, random.random()-0.1], screen, yellow_bullet))
    #     yellow_bullet = 0
    # if lime_state and lime_bullet > 0:
    #     bullet_list.append(Bullet(
    #         blocks_list[-1][0].x+BLOCK_WIDTH*1, blocks_list[-1][0].y-BLOCK_WIDTH*0, 3, [random.random()-0.1, random.random()-0.9], screen, lime_bullet))
    #     lime_bullet=0
    # if blue_state and blue_bullet > 0:
    #     bullet_list.append(Bullet(
    #         blocks_list[-1][-1].x-BLOCK_WIDTH*0, blocks_list[-1][-1].y-BLOCK_WIDTH*0, 4, [random.random()-0.9, random.random()-0.9], screen, blue_bullet))
    #     blue_bullet = 0

    fps = int(1/(time.time()-t_time)*SPEED)
    t_time = time.time()
    fps_text = font.render(
        "FPS: %i" % (fps), True, (255, 255, 255))
    screen.blit(fps_text, (TEXT_SIZE*0.5, (10*1+TEXT_SIZE*0)))

    # pygame.draw.rect(screen, (255, 255, 255),(440,20,10,10))

    # 更新屏幕内容
    pygame.display.flip()

    # if t:
    #     time.sleep(5)
    #     t = False


if __name__ == '__main__':
    # 设置主屏窗口
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.FULLSCREEN)
    # 设置窗口的标题，即游戏名称
    pygame.display.set_caption("SYSTEM-MEMZ-CAO")
    # 图标
    icon = pygame.image.load("icon.bmp").convert()
    pygame.display.set_icon(icon)

    blocks_list: list[list[Block]] = []
    for y in range(HEIGHT//BLOCK_WIDTH):
        temp = []
        for x in range(HEIGHT//BLOCK_WIDTH):
            c = 0
            # if HEIGHT//BLOCK_WIDTH*0.4<x<HEIGHT//BLOCK_WIDTH*0.6 and HEIGHT//BLOCK_WIDTH*0.4<y<HEIGHT//BLOCK_WIDTH*0.6:
            #     print(x-WIDTH//2, y-HEIGHT//2)
            # t=getDistance(x, y, WIDTH//2, HEIGHT//2)
            if getDistance((WIDTH-HEIGHT)//2+x*BLOCK_WIDTH, y*BLOCK_WIDTH, WIDTH//2, HEIGHT//2) < HEIGHT*0.1:
                c = 0
            elif not x//(HEIGHT//BLOCK_WIDTH//2) and not y//(HEIGHT//BLOCK_WIDTH//2):
                c = 1
            elif x//(HEIGHT//BLOCK_WIDTH//2) and not y//(HEIGHT//BLOCK_WIDTH//2):
                c = 2
            elif not x//(HEIGHT//BLOCK_WIDTH//2) and y//(HEIGHT//BLOCK_WIDTH//2):
                c = 3
            elif x//(HEIGHT//BLOCK_WIDTH//2) and y//(HEIGHT//BLOCK_WIDTH//2):
                c = 4
            # w = HEIGHT*0.5
            # if getDistance((WIDTH-HEIGHT)//2+x*BLOCK_WIDTH, y*BLOCK_WIDTH, WIDTH//2, HEIGHT//2) < HEIGHT*0.1:
            #     c = 0
            # elif getDistance((WIDTH-HEIGHT)//2+x*BLOCK_WIDTH, y*BLOCK_WIDTH, (WIDTH-HEIGHT)//2, 0) < w:
            #     c = 1
            # elif getDistance((WIDTH-HEIGHT)//2+x*BLOCK_WIDTH, y*BLOCK_WIDTH, WIDTH-(WIDTH-HEIGHT)//2, 0) < w:
            #     c = 2
            # elif getDistance((WIDTH-HEIGHT)//2+x*BLOCK_WIDTH, y*BLOCK_WIDTH, (WIDTH-HEIGHT)//2, HEIGHT) < w:
            #     c = 3
            # elif getDistance((WIDTH-HEIGHT)//2+x*BLOCK_WIDTH, y*BLOCK_WIDTH, WIDTH-(WIDTH-HEIGHT)//2, HEIGHT) < w:
            #     c = 4

            temp.append(
                Block(x*BLOCK_WIDTH+((WIDTH-HEIGHT)//2), y*BLOCK_WIDTH, c, screen, 32))
        blocks_list.append(temp)

    # for y in range(HEIGHT//BLOCK_WIDTH):
    #     temp = []
    #     for x in range(HEIGHT//BLOCK_WIDTH):
    #         c = 0
    #         if not x//(HEIGHT//BLOCK_WIDTH//2) and not y//(HEIGHT//BLOCK_WIDTH//2):
    #             c = 1
    #         elif x//(HEIGHT//BLOCK_WIDTH//2) and not y//(HEIGHT//BLOCK_WIDTH//2):
    #             c = 2
    #         elif not x//(HEIGHT//BLOCK_WIDTH//2) and y//(HEIGHT//BLOCK_WIDTH//2):
    #             c = 3
    #         elif x//(HEIGHT//BLOCK_WIDTH//2) and y//(HEIGHT//BLOCK_WIDTH//2):
    #             c = 4
    #         Block(x*BLOCK_WIDTH+((WIDTH-HEIGHT)//2), y *
    #               BLOCK_WIDTH, c, screen, 255).draw(screen)

    ball_list: list[Ball] = []
    for i in range(BALL_NUM):
        for c in range(1, 5):
            def y(_): return -(random.random()*(HEIGHT*0.375)+HEIGHT*0.125*0)
            if c in [1, 3]:
                # x = (WIDTH-HEIGHT)//2//2
                def x(_): return (random.random() *
                                  ((WIDTH-HEIGHT)//2-BLOCK_WIDTH*2)+BLOCK_WIDTH)
            elif c in [2, 4]:
                # x = WIDTH-(WIDTH-HEIGHT)//2//2
                def x(_): return (WIDTH-random.random() *
                                  ((WIDTH-HEIGHT)//2-BLOCK_WIDTH*2)+BLOCK_WIDTH)
            ball_list.append(Ball(x, y, c, screen))

    bullet_list: list[Bullet] = []
    # bullet_list.append(Bullet(
    #     blocks_list[0][0].x+BLOCK_WIDTH*2, blocks_list[0][0].y+BLOCK_WIDTH*2, 1, [1, 1], screen))

    pen_list: list[Pen] = []

    up_list: list[Up] = []
    for _ in range(UP_START_NUM):
        up_list.append(Up(WIDTH//2, HEIGHT//2))

    update()

    # keyboard.wait('space')
    # def x(x):
    #     global state
    #     if x.scan_code == 57: # space
    #         state = True
    # keyboard.hook(x)

    while 1:
        # 循环获取事件，监听事件状态
        for event in pygame.event.get():
            # 判断用户是否点了"X"关闭按钮,并执行if代码段
            if event.type == pygame.QUIT:
                # 卸载所有模块
                pygame.quit()
                # 终止程序，确保退出程序
                sys.exit()
        with open("./start.txt", "r") as f:
            r = f.read()
            # print(str([r])[1:-1])
            if "start" in r:
                break
        time.sleep(1.0)

    # t=True
    # 固定代码段，实现点击"X"号退出界面的功能，几乎所有的pygame都会使用该段代码
    start_time = time.time()
    while True:
        # t2=time.time()
        # print(time.time()-t2>1)
        # if time.time()-t2>1:
        update()
        if red_state+yellow_state+lime_state+blue_state <= 1:
            # break

            with open("./end.txt", "w") as f:
                f.write("end")

            # # 卸载所有模块
            # pygame.quit()
            # # 终止程序，确保退出程序
            # sys.exit()
