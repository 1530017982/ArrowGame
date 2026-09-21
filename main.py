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


# ======================
# 颜色
# ======================

WHITE = (255,255,255)
BLACK = (0,0,0)

BLUE = (50,120,255)

RED = (255,80,80)

GREEN = (50,200,100)

GRAY = (220,220,220)


# ======================
# 字体
# ======================

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
# 按钮
# ======================


restart_button = pygame.Rect(
    600,
    50,
    120,
    50
)


undo_button = pygame.Rect(
    600,
    100,
    120,
    50
)




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


history = []


state = "start"



shake = {}




# ======================
# 撤销功能
# ======================


def save_state():

    state = {

        "alive":
        [
            a.alive
            for a in arrows
        ],

        "mistakes":
        mistakes

    }


    history.append(state)




def undo():

    global mistakes


    if len(history)>0:


        state = history.pop()


        for i,a in enumerate(arrows):

            a.alive = state["alive"][i]


        mistakes = state["mistakes"]
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


        self.row = row

        self.col = col

        self.direction = direction


        self.x = 250 + col * 100

        self.y = 180 + row * 100


        self.alive = True


        self.offset = 0


        self.color = BLUE




    def draw(self):


        if not self.alive:

            return



        x = self.x + self.offset



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



        text = font.render(

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



    arrows = []


    mistakes = 5



    history.clear()



    data = levels[level_index]



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


        if a == target or not a.alive:

            continue



        # 向右

        if target.direction == "R":


            if (

                a.row == target.row

                and a.col > target.col

            ):

                return True





        # 向左

        if target.direction == "L":


            if (

                a.row == target.row

                and a.col < target.col

            ):

                return True





        # 向上

        if target.direction == "U":


            if (

                a.col == target.col

                and a.row < target.row

            ):

                return True





        # 向下

        if target.direction == "D":


            if (

                a.col == target.col

                and a.row > target.row

            ):

                return True




    return False





# ======================
# 点击箭头
# ======================


def click_arrow(pos):


    global mistakes



    for a in arrows:


        if not a.alive:

            continue



        rect = pygame.Rect(

            a.x,

            a.y,

            80,

            80

        )



        if rect.collidepoint(pos):



            if blocked(a):


                mistakes -= 1


                a.color = RED


                a.offset = 15


                shake[a] = 10




            else:


                save_state()


                a.alive = False



            break






# ======================
# 动画
# ======================


def update_animation():


    for a in list(shake):


        if shake[a] > 0:


            a.offset *= -1


            shake[a] -= 1



        else:


            a.offset = 0


            a.color = BLUE


            del shake[a]
            # ======================
# 绘制按钮
# ======================


def draw_button(
    rect,
    text,
    color
):


    pygame.draw.rect(

        screen,

        color,

        rect,

        border_radius=10

    )


    t = font.render(

        text,

        True,

        WHITE

    )


    screen.blit(

        t,

        (
            rect.x+20,
            rect.y+10
        )

    )





# ======================
# 绘制游戏界面
# ======================


def draw_game():


    screen.fill(WHITE)



    # 标题

    title = big_font.render(

        "一箭又一箭",

        True,

        BLACK

    )


    screen.blit(

        title,

        (250,20)

    )



    # 信息


    info = font.render(

        "第{}关   剩余箭头:{}   失误:{}".

        format(

            level_index+1,

            sum(

                1 for a in arrows

                if a.alive

            ),

            mistakes

        ),

        True,

        BLACK

    )


    screen.blit(

        info,

        (30,120)

    )



    # 箭头


    for a in arrows:

        a.draw()



    # 按钮


    draw_button(

        restart_button,

        "重新开始",

        GREEN

    )


    draw_button(

        undo_button,

        "撤销",

        BLUE

    )





# ======================
# 通关检查
# ======================


def check_win():


    global level_index

    global state



    if all(

        not a.alive

        for a in arrows

    ):


        level_index += 1



        if level_index >= len(levels):


            state = "win"


        else:


            load_level()






def draw_start():


    screen.fill(WHITE)



    title = big_font.render(

        "一箭又一箭",

        True,

        BLACK

    )


    screen.blit(

        title,

        (220,200)

    )



    tip = font.render(

        "点击开始游戏",

        True,

        BLACK

    )


    screen.blit(

        tip,

        (280,300)

    )





def draw_end(text):


    screen.fill(WHITE)


    t = big_font.render(

        text,

        True,

        BLACK

    )


    screen.blit(

        t,

        (220,250)

    )


    tip = font.render(

        "点击重新开始",

        True,

        BLACK

    )


    screen.blit(

        tip,

        (280,330)

    )





# ======================
# 主循环
# ======================


running = True



while running:



    for event in pygame.event.get():


        if event.type == pygame.QUIT:

            running = False



        if event.type == pygame.MOUSEBUTTONDOWN:



            pos = pygame.mouse.get_pos()



            # 开始界面

            if state == "start":


                state = "game"


                load_level()



            # 游戏

            elif state == "game":



                if restart_button.collidepoint(pos):


                    load_level()



                elif undo_button.collidepoint(pos):


                    undo()



                else:


                    click_arrow(pos)



            # 结束

            elif state == "win":


                level_index = 0


                state = "game"


                load_level()





    update_animation()



    if state == "game":


        check_win()


        draw_game()



    elif state == "start":


        draw_start()



    elif state == "win":


        draw_end(

            "恭喜通关!"

        )



    pygame.display.update()



    clock.tick(60)




pygame.quit()

sys.exit()