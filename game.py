import pygame
import numpy as np
from enum import Enum
import sys

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

CHOICE_LUX = GAMEWIDTH + 3
CHOICE_LUY = GAMEHEIGHT + 3
# def
pygame.font.init()
font = pygame.font.SysFont('microsoft Yahei', 16)


class MODE(Enum):
    INFO = 1
    WARNING = 2
    CHOICE = 3
    NONE = 4



def draw_rect(screen ,x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, 0)

def draw_point(screen, x, y, color):
    rect = pygame.Rect(20 * x + 1, 20 * y + 1, BLOCKSIZE - 1 , BLOCKSIZE - 1)
    pygame.draw.rect(screen, color, rect, 0)

def draw_card(screen, x, y, card):
    pass

def draw_grid(screen, grid):
    for x, heng in enumerate(grid):
        for y, point in enumerate(heng):
            if point:
                color = RED
            else:
                color = BLACK
            draw_point(screen, x, y, color)

def print_message(screen, x, y, message, color, mode:MODE):
    text = font.render(message, False, color)
    text_rect = text.get_rect()
    w = text_rect.w // 2
    h = text_rect.h // 2
    if mode == MODE.INFO:
        global INFO_NUM
        y += INFO_NUM * text_rect.h
        INFO_NUM += 1

    text_rect.center = (x + w + 3, y + h)
    screen.blit(text, text_rect)


def print_INFO(screen, message, color):
    x = INFO_LUX
    y = INFO_LUY
    print_message(screen, x, y, message, color, MODE.INFO)

def print_WARNING(screen, message, color):
    x = WARNING_LUX
    y = WARNING_LUY
    print_message(screen, x, y, message, color, MODE.WARNING)

def print_CHOICE(screen, message, color):
    x = CHOICE_LUX
    y = CHOICE_LUY
    print_message(screen, x, y, message, color, MODE.CHOICE)
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



def gaming():
    a = np.load('./a.npy')
    a = a.T
    # print(a)

    # a = cv2.resize(a, (150, 450))
    pygame.init()



    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Sab')


    done = False
    clock = pygame.time.Clock()
    surf = pygame.surfarray.make_surface(a)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # game

        # draw
        global INFO_NUM
        INFO_NUM = 0

        # screen.fill(WHITE)
        # draw_grid(screen)

        # draw_point(screen, 3,3)
        draw_grid(screen, a)

        # print_message(screen, 300, 300, 'hello', RED)
        print_INFO(screen, 'hello', RED)
        print_INFO(screen, 'hello', RED)
        print_INFO(screen, 'hello', RED)
        print_INFO(screen, 'hello', RED)
        print_WARNING(screen, 'Jesus ', WHITE)
        print_CHOICE(screen, 'choice', WHITE)

        for x in range(BLOCKWIDTH):
            pygame.draw.line(screen, WHITE, (x * BLOCKSIZE, 0), (x * BLOCKSIZE, GAMEHEIGHT), 1)
        for y in range(BLOCKHEIGHT):
            pygame.draw.line(screen, WHITE, (0, y * BLOCKSIZE), (GAMEWIDTH, y * BLOCKSIZE), 1 )
        # pygame.display.flip()
        pygame.draw.line(screen, GREEN, (GAMEWIDTH, 0), (GAMEWIDTH, HEIGHT), 3)
        pygame.draw.line(screen, GREEN, (0, GAMEHEIGHT), (WIDTH, GAMEHEIGHT  ), 3)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
# a = np.load('./a.npy')
# print(a.shape)
if __name__ == '__main__':
    gaming()