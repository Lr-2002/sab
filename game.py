import pygame
import numpy as np
from enum import Enum
import sys
import pygame_textinput

import game
from main import *
import copy

SIZE = (700, 500)
WIDTH = SIZE[0]
HEIGHT = SIZE[1]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255, 51, 204)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 204, 255)
GLD = (252, 186, 3)
GRAY = (158, 155, 147)
COLOR_LIST = [WHITE, RED, YELLOW, PINK, BLUE, GREEN, LIGHT_BLUE, GRAY, GLD]

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
CHOICE_NUM = 0
# def

CARD_CHOOSING = 0

text_input = pygame_textinput.TextInputVisualizer()
text_input.value = ''
text_input.font_color = WHITE
text_input.cursor_visible = True
pygame.font.init()
font = pygame.font.SysFont('microsoft Yahei', 16)


class Status(Enum):
    start = 1
    game = 2
    add_player = 3


class Game_Status(Enum):
    init = 0
    choose_card = 1
    choose_position = 2
    throw = 3
    pass_turn = 4
    re_choose_card = 5
    choose_player = 6
    choose_end = 7
    find_end = 8
    over = 9


class Tool_Status(Enum):
    one_tool = 1
    double_tool = 2


class PRINT_MODE(Enum):
    INFO = 1
    WARNING = 2
    CHOICE = 3
    NONE = 4
    CENTER = 5


def draw_rect(screen, x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, 0)


def draw_point(screen, x, y, color):
    rect = pygame.Rect(20 * x + 1, 20 * y + 1, BLOCKSIZE - 1, BLOCKSIZE - 1)
    pygame.draw.rect(screen, color, rect, 0)


def card_check(a):
    if a == ' ':
        return False
    elif a != '(' and a != ')':
        # print(a)
        return True


def get_card(card='( E )(END)( D )'):
    card = str(card)
    if '|' in card or '-' in card or '+' in card:
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
        tt_lis = copy.deepcopy(return_list)
        for x, tmp in enumerate(return_list):
            for y, point in enumerate(tmp):
                tt_lis[y][x] = return_list[x][y]
        return tt_lis
    elif 'MAP' in card:
        return [[2] * 3 for x in range(3)]
    elif 'ATT' in card:
        return [[3] * 3 for x in range(3)]
    elif 'DEF' in card:
        return [[4] * 3 for x in range(3)]
    elif 'TON' in card:
        return [[7] * 3 for x in range(3)]
    elif 'T' in card and 'F' in card and 'A' in card:
        return [[0] * 3 for x in range(3)]
    elif 'G' in card and 'L' in card and 'D' in card:

        return [[8] * 3 for x in range(3)]

    elif 'L' or 'P' or 'C' in card:
        return [[5] * 3 for x in range(3)]


def draw_grid_content(screen, grid):
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
    # print(card)
    # card = game.get_now_player().get_original_position(index)
    color_list = get_card(card)
    x = index * (BLOCKSIZE * 3 + 10) + CARD_LUX
    y = CARD_LUY
    card_center_x = int(x + BLOCKSIZE * 1.5)
    card_center_y = int(y + BLOCKSIZE * 3) + 20
    print_message(screen, card_center_x, card_center_y, str(index), WHITE, mode=PRINT_MODE.CENTER)
    for xx, lis in enumerate(color_list):
        for yy, color in enumerate(lis):
            color = COLOR_LIST[color]

            # print(color)

            draw_rect(screen, x + xx * BLOCKSIZE, y + yy * BLOCKSIZE, BLOCKSIZE - 1, BLOCKSIZE - 1, color)


def print_message(screen, x, y, message, color, mode: PRINT_MODE):
    text = font.render(message, False, color)
    text_rect = text.get_rect()
    w = text_rect.w // 2
    h = text_rect.h // 2
    if mode != PRINT_MODE.CENTER:
        if mode == PRINT_MODE.INFO:
            global INFO_NUM
            y += INFO_NUM * text_rect.h
            INFO_NUM += 1
        elif mode == PRINT_MODE.CHOICE:
            global CHOICE_NUM
            y += CHOICE_NUM * text_rect.h
            CHOICE_NUM += 1

        text_rect.center = (x + w + 3, y + h)
        screen.blit(text, text_rect)
    else:
        text_rect.center = (x, y)
        screen.blit(text, text_rect)


def print_INFO(screen, message, color=WHITE):
    x = INFO_LUX+2
    y = INFO_LUY
    print_message(screen, x, y, message, color, PRINT_MODE.INFO)


def print_WARNING(screen, message, color=WHITE):
    x = WARNING_LUX
    y = WARNING_LUY
    print_message(screen, x, y, message, color, PRINT_MODE.WARNING)


def print_CHOICE(screen, message, color=WHITE):
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
        if player.has_cards():
            print_INFO(screen, str(player) + ' {} {} '.format(player.trapped() ,player.has_gold()), WHITE)
        else:
            print_INFO(screen, str(player), WHITE)


def get_27_15(a: np.array):
    a = np.array(a)
    tmp = []
    for i in range(9):
        x = i * 5 + 2
        tmp += [x - 1, x, x + 1]
    # print(tmp)
    a = a.T
    a = a[tmp]
    return a


def read_input(events: pygame.event):
    # print(events)
    for event in events:
        # print(event['key'])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                value = text_input.value
                text_input.value = ''
                return value


def show_player_card(screen):
    person = game.get_now_player()
    print_WARNING(screen, '{}, You have these cards,  {} to throw and {} to pass'.format(person, person.card_num(), person.card_num() + 1), WHITE)
    cards = person.show_card()
    for index, card in enumerate(cards):
        draw_card(screen, index, str(card))
        if isinstance(card, BadTool) or isinstance(card, GoodTool):
            print_INFO(screen, '{} card is {}'.format(index, str(card)[5:10]), RED)


def draw_base_grid(screen):
    for x in range(BLOCKWIDTH):
        pygame.draw.line(screen, WHITE, (x * BLOCKSIZE, 0), (x * BLOCKSIZE, GAMEHEIGHT), 1)
    for y in range(BLOCKHEIGHT):
        pygame.draw.line(screen, WHITE, (0, y * BLOCKSIZE), (GAMEWIDTH, y * BLOCKSIZE), 1)
    # pygame.display.flip()
    pygame.draw.line(screen, GREEN, (GAMEWIDTH, 0), (GAMEWIDTH, HEIGHT), 3)
    pygame.draw.line(screen, GREEN, (0, GAMEHEIGHT), (WIDTH, GAMEHEIGHT), 3)


def draw_text(screen):
    screen.blit(text_input.surface, (CHOICE_LUX, CHOICE_LUY + 50))


def end_show(clock, time=10):
    pygame.display.update()
    # print(time)
    clock.tick(time)


def handle_event():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    return events


def circle_init(screen, grid):
    global INFO_NUM
    INFO_NUM = 0
    global CHOICE_NUM
    CHOICE_NUM = 0
    draw_grid_content(screen, grid)
    draw_base_grid(screen)
    draw_text(screen)


def get_position(posi):
    try:
        posi1, posi2 = posi.strip().split(',')
    except ValueError:
        posi1, posi2 = posi.strip().split('，')

    posi1 = posi1.strip().split('(')[0]
    posi1 = int(posi1)
    posi2 = posi2.strip().split(')')[0]
    posi2 = int(posi2)
    return posi1, posi2


def gaming():
    mode = 'release'

    # a = np.load('./a.npy')
    # a = get_27_15(a)
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Sab')
    RIGHT = False
    done = False
    clock = pygame.time.Clock()
    print_INFO(screen, 'Welcome to the game!', WHITE)
    status = Status.start
    game_status = Game_Status.init

    if mode == 'deve':
        game.distribute_card()
        status = Status.game

    card_num = 0

    double_card_card = None

    round = 0
    tool_status = Tool_Status.one_tool

    show_end_card_timing = 0
    show_end_card_bool = False
    show_end_card_card = None
    while not done:
        print(status)
        time = 10
        screen.fill(BLACK)
        events = handle_event()
        text_input.update(events)
        circle_init(screen, get_27_15(game.get_grid_map()))


        # show_player(screen)

        if status == Status.start:
            print_INFO(screen, 'Welcome')
            print_INFO(screen, 'Please enter ')
            print_INFO(screen, 'players number')
            print_CHOICE(screen, 'Enter num here')

            inp = read_input(events)
            if inp is not None:
                inp = int(inp)
                game.players_num = inp
                status = Status.add_player
                if game.get_player_num() == 0:
                    game.make_actor_list()
                    game.init()
                    game.distribute_card()
                    status = Status.add_player
                else:
                    game.distribute_card()
                    status = Status.add_player
        elif status == Status.add_player:
            show_player(screen)
            if game.get_player_num() < game.players_num:
                print_CHOICE(screen, 'name, 0 or 1')
                inp = read_input(events)
                if inp is not None:
                    print(game.add_player_gui(inp))
            else:
                game.distribute_card()
                status = Status.game
        elif status == Status.game:
            print_CHOICE(screen, 'your choose is as below', WHITE)

            print_INFO(screen, 'This is Round {}'.format(round))
            show_player(screen)
            # show_player_card(screen)
            player = game.get_now_player()
            if game_status == Game_Status.init:
                show_player_card(screen)
                print_CHOICE(screen, 'Input your card num')
                inp = read_input(events)
                if inp is not None:
                    inp = int(inp)
                    if inp < game.get_now_player().card_num():
                        card_num = inp
                        if isinstance(game.get_now_player().get_showed_card(card_num), Path):
                            game_status = Game_Status.choose_position
                        elif isinstance(game.get_now_player().get_showed_card(card_num), Tafang):
                            game_status = Game_Status.choose_position
                        elif isinstance(game.get_now_player().get_showed_card(card_num), Ditu):
                            game_status = Game_Status.choose_end
                        else:
                            game_status = Game_Status.choose_player
                    elif inp == game.get_now_player().card_num():
                        game_status = Game_Status.throw
                        # throw_card()
                    else:
                        game_status = Game_Status.pass_turn
                        # pass_turn()

            elif game_status == Game_Status.throw:
                show_player_card(screen)
                print_WARNING(screen, 'choose your card to be thrown')
                print_CHOICE(screen, 'input card num ')
                inp = read_input(events)
                if inp is not None:
                    inp = int(inp)
                    card = game.get_now_player().get_showed_card(inp)
                    game.get_now_player().pop_card(card_num)
                    game.next_player()
                    game_status = Game_Status.init
            elif game_status == Game_Status.pass_turn:
                game.next_player()
                game_status = Game_Status.init
            elif game_status == Game_Status.choose_position or game_status == Game_Status.re_choose_card:
                if game_status == Game_Status.re_choose_card:
                    print_CHOICE(screen, 'Rechoose your card')
                print_WARNING(screen, 'You have choose this card')
                draw_card(screen, card_num, str(player.get_card(card_num)))
                print_CHOICE(screen, 'Input your position, x,y')
                inp = read_input(events)
                if inp is not None:
                    x, y = get_position(inp)
                    if game.push_card(x, y, player.get_card(card_num)):
                        player.pop_card(card_num)
                        game.next_player()
                        if game.find_gold():
                            round += 1
                            status = Status.start
                            game.find_end()
                            game_status = Game_Status.find_end
                            end_show(time)
                            continue
                        game_status = Game_Status.init
                    else:
                        game_status = Game_Status.re_choose_card
            elif game_status == Game_Status.choose_player:
                card = player.get_showed_card(card_num)
                if isinstance(card, Double_tool):
                    tool_status = Tool_Status.double_tool
                if tool_status == Tool_Status.one_tool:
                    card = game.get_now_player().get_showed_card(card_num)
                    if double_card_card is not None:
                        card = double_card_card
                        # draw_card(screen, 0, str(card))
                    draw_card(screen, card_num, str(card))
                    print_CHOICE(screen, 'Choose your target')
                    print_WARNING(screen, 'Please choose your target to use your card')
                    inp = read_input(events)
                    if inp is not None:
                        inp = int(inp)
                        game.get_player(inp).push_tool_cards(card)
                        print(len(game.get_player(inp).cards))
                        # input('1')
                        if double_card_card is None:
                            game.get_now_player().pop_card(card_num)
                        game.next_player()
                        game_status = Game_Status.init
                        double_card_card = None
                else:
                    print_WARNING(screen, 'You have these choose:{}'.format(str(game.get_now_player().get_showed_card(card_num))))
                    print_CHOICE(screen, 'L,C,P in your choice')
                    inp = read_input(events)
                    if inp is not None:
                        draw_card(screen, card_num, card='(   )( {} )(   )'.format(inp))
                        if inp.upper() == 'L':
                            card = Light()
                        elif inp.upper() == 'C':
                            card = Cart()
                        elif inp.upper() == 'P':
                            card = Pickaxe()
                        game.get_now_player().pop_card(card_num)
                        double_card_card = card
                    tool_status = Tool_Status.one_tool
            elif game_status == Game_Status.choose_end:
                if not show_end_card_bool:
                    print_WARNING(screen, 'Please choose a position to use this Map card')
                    print_CHOICE(screen, 'choose one:0,1,2')
                    inp = read_input(events)
                    if inp is not None:
                        # todo double use card
                        inp = int(inp)
                        posi = 0
                        if inp == 0:
                            posi = 1
                        elif inp == 1:
                            posi = 3
                        elif inp == 2:
                            posi = 5
                        card = game.show_end_card(posi, 9)
                        show_end_card_bool = True
                        show_end_card_card = card
                        game.get_now_player().pop_card(card_num)
                        game.next_player()
                else:
                    print_INFO(screen, ' this is the card you choose')
                    draw_card(screen, 0, show_end_card_card)
                    show_end_card_timing += 1
                    if show_end_card_timing == 10:
                        show_end_card_bool = False
                        show_end_card_card = None
                        show_end_card_timing = 0
                        game_status = Game_Status.init
            elif game_status == Game_Status.find_end:
                show_player(screen)
                print_INFO('round {} is over'.format(round), RED)
                if round == 2:
                    game_status = Game_Status.over
                    continue
                show_end_card_timing += 1
                if show_end_card_timing == 10:
                    show_end_card_timing = 0
                    game_status = Game_Status.init
            elif game_status == Game_Status.over:
                print_INFO(screen, 'Game is over', RED)
                show_player(screen)
                print_INFO(screen, '{} is the winner'.format(game.get_winner()))

        # todo: 2. choose card
        # todo: 3. choose position
        # todo: 4. choose player
        # todo: 5. end of the game

        end_show(clock, time)

    pygame.quit()


if __name__ == '__main__':
    gaming()

