import pygame
import numpy as np
from enum import Enum
import sys
import pygame_textinput
from main import game

SIZE = (700, 500)
WIDTH = SIZE[0]
HEIGHT = SIZE[1]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BLOCKSIZE = 20
BLOCKWIDTH = 28
BLOCKHEIGHT = 16
GAMEWIDTH = (BLOCKWIDTH - 1) * BLOCKSIZE
GAMEHEIGHT = (BLOCKHEIGHT - 1) * BLOCKSIZE

INFO_LUX = GAMEWIDTH
INFO_LUY = 0
INFO_NUM = 0

WARNING_LUX = 0
WARNING_LUY = GAMEHEIGHT + 3
CARD_LUX = 10
CARD_LUY = GAMEHEIGHT + 40

CHOICE_LUX = GAMEWIDTH + 3
CHOICE_LUY = GAMEHEIGHT + 3
# def

CARD_CHOOSING = 0

text_input = pygame_textinput.TextInputVisualizer()
text_input.value = 'tesing'
text_input.font_color = WHITE
text_input.cursor_visible = True
pygame.font.init()
font = pygame.font.SysFont('microsoft Yahei', 16)


class PRINT_MODE(Enum):
    INFO = 1
    WARNING = 2
    CHOICE = 3
    NONE = 4
    CENTER = 5



def draw_rect(screen ,x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, 0)

def draw_point(screen, x, y, color):
    rect = pygame.Rect(20 * x + 1, 20 * y + 1, BLOCKSIZE - 1 , BLOCKSIZE - 1)
    pygame.draw.rect(screen, color, rect, 0)

def card_check(a):
    if a == ' ':
        return False
    elif a != '(' and a != ')':
        # print(a)
        return True

def get_card(card='( E )(END)( D )'):
    end_list = []
    return_list = []
    for i in card:
        tmp = card_check(i)
        if tmp is not None:
            end_list.append(tmp)
    tt = []

    for index, tmp in enumerate(end_list):
        tt.append(tmp)
        if index % 3 == 2:
            return_list.append(tt)
            tt = []
    return return_list

def draw_grid(screen, grid):
    for x, heng in enumerate(grid):
        for y, point in enumerate(heng):
            if point:
                color = RED
            else:
                color = BLACK
            draw_point(screen, x, y, color)

def draw_card(screen, index, card):
    """

    :param screen:
    :param index: 第几张卡
    :param card:
    :return:
    """
    color_list = get_card(card)
    x = index * (BLOCKSIZE * 3 + 10) + CARD_LUX
    y = CARD_LUY
    card_center_x = int(x + BLOCKSIZE * 1.5)
    card_center_y = int(y + BLOCKSIZE * 3) + 20
    print_message(screen, card_center_x, card_center_y, str(index), WHITE, mode=PRINT_MODE.CENTER)
    for xx, lis in enumerate(color_list):
        for yy, color in enumerate(lis):
            if color:
                color = RED
            else:
                color = WHITE

            # print(color)

            draw_rect(screen, x + xx * BLOCKSIZE, y + yy * BLOCKSIZE, BLOCKSIZE-1, BLOCKSIZE-1, color)


def print_message(screen, x, y, message, color, mode:PRINT_MODE):
    text = font.render(message, False, color)
    text_rect = text.get_rect()
    w = text_rect.w // 2
    h = text_rect.h // 2
    if mode != PRINT_MODE.CENTER:
        if mode == PRINT_MODE.INFO:
            global INFO_NUM
            y += INFO_NUM * text_rect.h
            INFO_NUM += 1

        text_rect.center = (x + w + 3, y + h)
        screen.blit(text, text_rect)
    else:
        text_rect.center = (x, y)
        screen.blit(text, text_rect)


def print_INFO(screen, message, color):
    x = INFO_LUX + 10
    y = INFO_LUY
    print_message(screen, x, y, message, color, PRINT_MODE.INFO)

def print_WARNING(screen, message, color):
    x = WARNING_LUX
    y = WARNING_LUY
    print_message(screen, x, y, message, color, PRINT_MODE.WARNING)

def print_CHOICE(screen, message, color):
    x = CHOICE_LUX
    y = CHOICE_LUY
    print_message(screen, x, y, message, color, PRINT_MODE.CHOICE)
# def from_gird_to_map(grid, screen):
#     a = np.load('./a.npy')
#     block_size = 20
#     x, y = 0, 0
#     for x in range(a.shape[0]):
#         for y in range(a.shape[1]):
#             rect = pygame.Rect(x, y, block_size, block_size)
#             pygame.draw.rect(screen, WHITE if )
#             y += block_size
#         x += block_size

# def choose_card(screen, event):
#     index = CARD_CHOOSING
#     print_message(screen, inde)

def show_player(screen):
    print_INFO(screen, '-+-Players-+-', WHITE)
    for index, player in enumerate(game.players):
        print_INFO(screen, str(player), WHITE)

def get_27_15(a:np.array):
    tmp = []
    for i in range(9):
        x = i * 5 + 2
        tmp += [x - 1, x, x + 1]
    # print(tmp)
    a = a.T
    a = a[tmp]
    return a

def gaming():
    a = np.load('./a.npy')
    a = get_27_15(a)
    pygame.init()



    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Sab')
    RIGHT = False

    done = False
    clock = pygame.time.Clock()
    # screen.blit(text_input.surface, (CHOICE_LUX, CHOICE_LUY + 50))

    while not done:
        screen.fill(BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        text_input.update(events)
        print(text_input.value)



        # game

        # draw
        global INFO_NUM
        INFO_NUM = 0

        draw_grid(screen, a)

        print_WARNING(screen, 'Jesus ', WHITE)
        print_CHOICE(screen, 'choice', WHITE)

        draw_card(screen, 0, '( | )(-+-)(   )')
        draw_card(screen, 1, '( | )( +-)(   )')
        draw_card(screen, 2, '( | )(-+ )(   )')
        draw_card(screen, 3, '( | )(-+-)( | )')

        # INFO
        show_player(screen)


        for x in range(BLOCKWIDTH):
            pygame.draw.line(screen, WHITE, (x * BLOCKSIZE, 0), (x * BLOCKSIZE, GAMEHEIGHT), 1)
        for y in range(BLOCKHEIGHT):
            pygame.draw.line(screen, WHITE, (0, y * BLOCKSIZE), (GAMEWIDTH, y * BLOCKSIZE), 1 )
        # pygame.display.flip()
        pygame.draw.line(screen, GREEN, (GAMEWIDTH, 0), (GAMEWIDTH, HEIGHT), 3)
        pygame.draw.line(screen, GREEN, (0, GAMEHEIGHT), (WIDTH, GAMEHEIGHT  ), 3)



        screen.blit(text_input.surface, (CHOICE_LUX, CHOICE_LUY + 50))

        pygame.display.update()

        clock.tick(10)

    pygame.quit()
if __name__ == '__main__':
    gaming()
    # get_card()