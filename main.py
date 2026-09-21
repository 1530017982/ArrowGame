import pygame
import sys
import copy


pygame.init()


# ======================
# 游戏窗口
# ======================

WIDTH = 800
HEIGHT = 700

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "一箭又一箭"
)


# 颜色

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (50,120,255)
RED = (255,80,80)
GREEN = (50,200,100)
GRAY = (220,220,220)


font = pygame.font.SysFont(
    "SimHei",
    30
)


big_font = pygame.font.SysFont(
    "SimHei",
    50
)


clock = pygame.time.Clock()


# ======================
# 关卡设计
# ======================


levels = [

[
["R","R","U"],
[None,None,"D"],
["L",None,None]
],


[
["R",None,"R"],
["D","U","R"],
[None,None,"D"]
],


[
["R","R","R"],
["U","D","L"],
["L","D","D"]
]

]


# ======================
# 游戏变量
# ======================


level_index = 0

mistakes = 5


arrows = []


state = "start"


shake = {}


# ======================
# 箭头对象
# ======================


class Arrow:


    def __init__(
        self,
        row,
        col,
        direction
    ):

        self.row=row
        self.col=col
        self.direction=direction

        self.x=250+col*100
        self.y=180+row*100

        self.alive=True

        self.offset=0

        self.color=BLUE



    def draw(self):

        if not self.alive:
            return


        x=self.x+self.offset


        pygame.draw.rect(
            screen,
            GRAY,
            (
                self.x,
                self.y,
                80,
                80
            )
        )


        text=font.render(
            self.symbol(),
            True,
            self.color
        )

        screen.blit(
            text,
            (
                x+20,
                self.y+20
            )
        )


    def symbol(self):

        return {

            "U":"↑",
            "D":"↓",
            "L":"←",
            "R":"→"

        }[self.direction]



# ======================
# 加载关卡
# ======================


def load_level():

    global arrows
    global mistakes


    arrows=[]

    mistakes=5


    data=levels[level_index]


    for r,row in enumerate(data):

        for c,value in enumerate(row):

            if value:

                arrows.append(
                    Arrow(
                        r,
                        c,
                        value
                    )
                )



# ======================
# 判断阻挡
# ======================


def blocked(target):


    for a in arrows:


        if a==target or not a.alive:
            continue


        # 向右

        if target.direction=="R":

            if (
                a.row==target.row
                and a.col>target.col
            ):
                return True



        # 向左

        if target.direction=="L":

            if (
                a.row==target.row
                and a.col<target.col
            ):
                return True



        # 向上

        if target.direction=="U":

            if (
                a.col==target.col
                and a.row<target.row
            ):
                return True



        # 向下

        if target.direction=="D":

            if (
                a.col==target.col
                and a.row>target.row
            ):
                return True



    return False



# ======================
# 点击检测
# ======================

# 箭头移动检测
# 判断箭头同方向上的棋盘位置
# 如果存在其他箭头，则产生碰撞反馈
def click_arrow(pos):

    global mistakes


    for a in arrows:


        if not a.alive:
            continue


        rect=pygame.Rect(
            a.x,
            a.y,
            80,
            80
        )


        if rect.collidepoint(pos):


            if blocked(a):

                mistakes-=1

                a.color=RED

                a.offset=15


                shake[a]=10


            else:

                a.alive=False



# ======================
# 动画
# ======================


def update_animation():


    for a in list(shake):


        if shake[a]>0:

            a.offset*=-1

            shake[a]-=1


        else:

            a.offset=0
            a.color=BLUE

            del shake[a]



# ======================
# 绘制界面
# ======================


def draw_game():


    screen.fill(WHITE)


    title=font.render(

        f"第 {level_index+1} 关",

        True,

        BLACK

    )


    screen.blit(
        title,
        (30,30)
    )


    info=font.render(

        f"剩余箭头:{sum(a.alive for a in arrows)}   失误:{mistakes}",

        True,

        BLACK

    )


    screen.blit(
        info,
        (30,80)
    )


    for a in arrows:

        a.draw()



    pygame.draw.rect(

        screen,

        GREEN,

        (600,50,120,50)

    )


    screen.blit(

        font.render(
            "重新开始",
            True,
            BLACK
        ),

        (610,60)

    )



# ======================
# 开始界面
# ======================


def draw_start():

    screen.fill(WHITE)


    t=big_font.render(

        "一箭又一箭",

        True,

        BLUE

    )


    screen.blit(
        t,
        (250,200)
    )


    pygame.draw.rect(

        screen,

        GREEN,

        (300,350,200,70)

    )


    screen.blit(

        font.render(
            "开始游戏",
            True,
            BLACK
        ),

        (330,370)

    )



# ======================
# 结束界面
# ======================


def draw_end(win):


    screen.fill(WHITE)


    if win:

        text="通关成功"

    else:

        text="挑战失败"



    t=big_font.render(

        text,

        True,

        BLUE

    )


    screen.blit(
        t,
        (270,250)
    )


    screen.blit(

        font.render(
            "点击重新开始",
            True,
            BLACK
        ),

        (270,350)

    )



# ======================
# 主循环
# ======================


load_level()


while True:


    for event in pygame.event.get():


        if event.type==pygame.QUIT:

            pygame.quit()

            sys.exit()



        if event.type==pygame.MOUSEBUTTONDOWN:


            pos=pygame.mouse.get_pos()



            if state=="start":

                state="game"



            elif state=="game":


                if (
                    600<pos[0]<720
                    and 50<pos[1]<100
                ):

                    load_level()


                else:

                    click_arrow(pos)



    if state=="start":

        draw_start()


    elif state=="game":


        update_animation()


        draw_game()


        if mistakes<=0:

            state="fail"



        if all(
            not a.alive
            for a in arrows
        ):

            level_index+=1


            if level_index>=len(levels):

                state="win"

            else:

                load_level()



    elif state=="win":

        draw_end(True)


    elif state=="fail":

        draw_end(False)



    pygame.display.update()


    clock.tick(60)