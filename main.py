import os
import random
from collections import deque
from abc import ABCMeta, abstractmethod
import copy
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
__metaclass__ = ABCMeta
def cls():
    os.system('cls')

class DeGap:
    def __init__(self, degap1=False, degap2=False, degap3=False):
        """
        if degap is True, it will cancel the gap
        :param degap1:
        :param degap2:
        :param degap3:
        """
        self.degap1 = degap1
        self.degap2 = degap2
        self.degap3 = degap3

    def is_single_usage(self):
        return not(self.degap1 if self.degap1 == self.degap2 else self.degap3)

    def __repr__(self):
        return str(self.degap1)+str(self.degap2) + str(self.degap3)

    def choose(self, number):
        if number == 1:
            return DeGap(True)
        elif number == 2:
            return DeGap(degap2=True)
        elif number == 3 :
            return DeGap(degap3=True)

    def show(self):
        # show_card()
        print(self)
def str2list(str):
    return list(str)
class Gap:
    def __init__(self, gap1=False, gap2=False, gap3=False):
        """
        if gap is true ,it will stop someone from talking

        :param gap1:
        :param gap2:
        :param gap3:
        """
        self.gap1 = gap1
        self.gap2 = gap2
        self.gap3 = gap3

    def is_trapped(self):
        return self.gap1 or self.gap2 or self.gap3

    def __add__(self, other):
        self.gap1 += other.gap1
        self.gap2 += other.gap2
        self.gap3 += other.gap3
        return Gap(self.gap1, self.gap2, self.gap3)

    def __sub__(self, other: DeGap):
        if other.is_single_usage():
            return Gap(bool(self.gap1 - other.degap1), bool(self.gap2 - other.degap2), bool(self.gap3 - other.degap3))
        else:
            print('This card has two function, please choose one function to use')
            other.show()
            choosed = int(input('input card\'s number to choose'))
            choice = other.choose(choosed)
            # print(choice)
            return self-choice

    def __repr__(self):
        return str(self.gap1) +  str(self.gap2) +  str(self.gap3)

class Status:
    def __init__(self):
        self.passable = True
        self.gap = Gap()

    def update(self):
        self.passable = not self.gap.get_gap()

    def update_gap(self, gap):
        self.gap += gap
        self.update()



class Player:
    def __init__(self, name, actor, statue=True):
        cards = []
        self.name = name
        self.actor = actor
        self.cards = cards
        self.action_cards = []
        self.status = statue # False for AI , True for human
        self.choice = None # card
        self.gold = Gold(0)
        self.gold_list = []
        self.gap = Gap(False, False, False)

    def push_gold(self, gold):
        self.gold += gold
        self.gold_list.append(gold)

    def has_gold(self):
        return str(self.gold)

    def has_cards(self):
        return  len(self.cards) != 0

    def is_good(self):
        return self.actor.is_good()

    def choose(self):
        if self.has_cards():
            print('{}, You have these cards to select: '.format(self.name))
            self.show_card()
            num = input('Please choose your card to use, other number to pass the choose')
            num = int(num)
            if num < len(self.cards):
                card = self.cards[num]
                return card

            elif num == len(self.cards):
                # self.show_card()
                card = int(input('Choose the card to be thrown:'))
                self.cards.pop(card)
                print('You have these cards left: {}'.format(self.cards))
            else:
                return None
        else:
            print('You have no cards , turn to the next one ')
            return None

    def is_trapped(self):
        return self.gap.is_trapped()

    def update_action_cards(self):
        for i in self.cards:
            if isinstance(i, Action):
                self.action_cards.append(i)

    def show_card(self):
        show = ''
        self.update_action_cards()
        tmp = 0
        # todo change the show path into three lines
        if not self.is_trapped():
            for index, card in enumerate(self.cards):
                print(index, card, end=' ,')
                tmp = index
            print(tmp+1, 'Throw away a card', end=' ,')
            print(tmp+2, 'Pass')
        else:
            for index, card in enumerate(self.action_cards):
                print(index, card, end=' ,')
                tmp = index
            print(tmp + 1, 'Throw away a card', end=' ,')
            print(tmp + 2, 'Pass')

        return show

    def add_card_list(self, cards):
        for i in cards:
            self.add_card(i)

    def add_card(self, card):
        self.cards.append(card)
        card.belong = self
    def __repr__(self):
        return self.name + '(Human)' if self.status else '(AI)'

    def push_tool_cards(self, card):
        if isinstance(card, BadTool):
            self.gap +  card.gap
        elif isinstance(card, GoodTool):
            self.gap -= card.decap

class Card:
    def __init__(self):
        self.orientation = True # true for zheng; false for fan
        self.used = False
        self.usage = []

    def change_belong(self, player: Player):
        self.belong = player

    def __setitem__(self, key, value):
        if key < len(self.usage):
            self.usage[key] = value

    def __getitem__(self, item):
        if item < len(self.usage):
            return self.usage[item]

    def is_used(self):
        return self.used

    def is_zheng(self):
        return self.orientation

    def is_gap(self):
        return False

    def is_degap(self):
        return False

    def __repr__(self):
        return self.usage if self.usage is not None else '(   )(   )(   )'

    @abstractmethod
    def use(self):
        pass

    def show(self):
        cnt = 1
        for i in self.usage:
            if cnt == 5:
                print(i)
                cnt = 1
            else:
                print(i, end='')
                cnt += 1





def show_card(card:Card):
    # todo use three lines to show
    pass

def get_x(x):
    return 3 * x - 2

def get_y(y):
    return 5 * y - 3

class End(Card):
    def __init__(self, gold=False):
        super(End, self).__init__()
        self.usage = '( E )(END)( D )'
        self.gold = gold
        self.x = 0
        self.y = 0
        self.is_find = False

    def change_position(self, x, y):
        self.x = x
        self.y = y

    def found(self):
        self.is_find = True
        if self.gold:
            self.usage = '( G )( L )( D )'
            return True
        else:
            self.usage = '( S )(TON)( E )'
            return False

    def is_gold(self):
        return self.gold

    def __repr__(self):
        return '(   )(GLD)(   )' if self.gold else '( S )(TON)( E )'

class Empty(Card):
    def __init__(self):
        super(Empty, self).__init__()
        self.usage='(   )(   )(   )'

class Point:
    def __init__(self, status=Status, is_card=False):

        self.is_card = is_card
        self.card = Card()
        self.status = status


    def is_carded(self):
        return self.is_card

    def __repr__(self):
        return 'X' if self.is_card else ' '

    def push_card(self, card: Card):
        self.card = card
        self.is_card = True
        if self.card.is_gap():
            self.status.update_gap(card.gap)
        elif self.card.is_degap():
            pass
            # self.status.update_gap(card.)

class Start(Card):
    def __init__(self):
        super(Start, self).__init__()
        self.usage='( | )(-S-)( | )'
        self.x = 0
        self.y = 0
        # print(self.usage)
    def change_position(self, x, y):
        self.x = x
        self.y = y

class Action(Card):
    def __init__(self, n=True):
        super(Action, self).__init__()
        self.n = n
        self.position = Point()

    def use(self):
        print('Please choose someone to use your card')
        game.show_players()
        person = int(input('Please input the guys you choose to use this card'))
        person = game.get_player(person)
        person.push_tool_cards(self)

class GoodTool(Action):
    def __init__(self, degap:DeGap, n=True):
        super(GoodTool, self).__init__(n)
        self.decap = degap

    def work_on(self, target:Player):
        target.gap += self.decap
    def is_degap(self):
        return True

    def is_gap(self):
        return False


class BadTool(Action):
    def __init__(self, gap:Gap):
        super(BadTool, self).__init__()
        self.gap = gap

    def work_on(self, target:Player):
        target.gap = self.gap

    def is_gap(self):
        return True

    def is_degap(self):
        return False

    def __sub__(self, other:GoodTool):
        self.gap = self.gap - other.decap



class Ditu(Action):
    def __init__(self):
        super(Ditu, self).__init__()
        self.usage = '( M )(MAP)( P )'
    # def show_ditu(self):
    #     pass

    def use(self):
        x, y =choose_position('There is three card in the map (1, 9), (3, 9), (5, 9), please choose your position to view')
        game.show_end_card(x, y)
        input('enter to pass')
def choose_position(intro = 'Please choose a position to use this card'):
    print(intro)
    posi = input('Input your position in this type x, y split by comma')
    posi1, posi2 = posi.strip().split(',')
    posi1 = posi1.strip().split('(')[0]
    posi1 = int(posi1)
    posi2 = posi2.strip().split(')')[0]
    posi2 = int(posi2)
    return (posi1, posi2)

class Tafang(Action):
    def __init__(self):
        super(Tafang, self).__init__()
        self.usage = '( T )( A )( F )'

    def use(self):
        x, y = choose_position()
        empty = Empty()
        game.push_card(x, y, empty)

class Broken_light(BadTool):
    def __init__(self):
        super(Broken_light, self).__init__(gap=Gap(True, False, False))
        self.usage = '(ATT)( L )(   )'

class Broken_cart(BadTool):
    def __init__(self):
        super(Broken_cart, self).__init__(gap=Gap(False, True, False))
        self.usage = '(ATT)( C )(   )'


class Broken_pickaxe(BadTool):
    def __init__(self):
        super(Broken_pickaxe, self).__init__(gap=Gap(False, False, True))
        self.usage = '(ATT)( P )(   )'


class Light(GoodTool):
    def __init__(self):
        super(Light, self).__init__(degap=DeGap(True, False, False))
        self.usage = '(DEF)( L )(   )'


class Cart(GoodTool):
    def __init__(self):
        super(Cart, self).__init__(degap=DeGap(False, True, False))
        self.usage = '(DEF)( C )(   )'


class Pickaxe(GoodTool):
    def __init__(self):
        super(Pickaxe, self).__init__(degap=DeGap(False, False, True))
        self.usage = '(DEF)( P )(   )'


class Double_tool(GoodTool):
    def __init__(self, gap1=False, gap2=False, gap3=False):
        super(Double_tool, self).__init__(degap=DeGap(gap1, gap2, gap3))
        self.usage = '(   )({}{}{})(   )'.format('L' if gap1 else ' ', 'C' if gap2 else ' ', 'P' if gap3 else ' ')


def show_list(head, lis):
    print(head, end='|')
    for i in lis:

        print(i, end='')
    print()
def show_list_without(head, lis):
    print(head, end=' ')
    for i in lis:

        print(i, end=' ')
    print()
class Actor(Card):
    def __init__(self, actor=True):
        """
        :param actor: True for good and False for bad
        """
        super(Actor, self).__init__()
        self.actor = actor # true stand for the good and False for the bad
    def is_good(self):
        return self.actor

    def is_bad(self):
        return not self.actor

    def __repr__(self):
        return str(self.actor)

    def __eq__(self, other):
        if self.actor == other.actor:
            return True
        else:
            return False

class Map:
    def __init__(self, h=5, w=9):
        self.h = h
        self.w = w
        self.grid = [[Point() for x in range(w)] for y in range(h)]
        self.chessboard = [[' ' for x in range(w * 5)] for z in range(h*3)]
        self.grid_map = [[0 for x in range(w * 5)] for z in range(h * 3)]
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    def show_chessboard(self):
        print('Here is the map,please')
        z = ['( '+ str(x) + ' )' for x in range(1,10)]
        show_list('     ',z)
        print()
        flag = 1
        for x in self.grid:
            show_list( '( '+ str(flag) + ' )', x)
            flag += 1
            print()

    def show_grid(self):
        print(' ', [x for x in range(len(self.grid[0]))])
        for x, grids in enumerate(self.grid):
            print(x, grids)

    def find_path(self, x1, y1, x2, y2):
        print(x1, y1, x2, y2)
        grid = Grid(matrix=self.grid_map)
        print('grid_map w', len(self.grid_map))
        print('grid_map h', len(self.grid_map[0]))
        path, runs = self.finder.find_path(grid.node(x1, y1), grid.node(x2, y2), grid)
        # print('operations:', runs, 'path length:', len(path))

        if len(path) != 0:
            return True
        else:
            return False

    def chess_w(self):
        return len(self.chessboard[0])

    def chess_h(self):
        return len(self.chessboard)

    def show(self):
        flag = 1
        num = 1
        cnt = 1
        print('Current mine state:')
        z = ['( '+ str(x) + ' )' for x in range(1,10)]
        show_list('     ',z)
        print('-----+'+ '-'*(self.w * 5 ))
        for i in self.chessboard:
            if num % 3  == 2 :
                show_list('( ' + str(flag) + ' )', i)
                flag += 1
            else:
                show_list('(   )', i)


            num +=1
            cnt +=1
        # print(cnt)?


    def push_card(self, x, y, card :Card):
        if not self.grid[x-1][y-1].is_carded():
            self.grid[x-1][y-1].push_card(card)
            # tmp = copy.deepcopy(card)
            # tmp[0] = ' '
            # tmp[4] = ' '
            # tmp[10] = ' '
            # tmp[14] = ' '
            tx = x * 3 - 2
            ty = y * 5 - 3
            cnt = 0
            for xx in range(tx-1, tx+2):
                for yy in range(ty-2, ty+3):
                    # print(xx, yy, card[cnt])
                    self.chessboard[xx][yy] = card[cnt]
                    if cnt not in [0, 4, 10, 14]:
                        if card[cnt] != ' ':
                            self.grid_map[xx][yy] = 1
                        else:
                            self.grid_map[xx][yy] = 0
                    cnt += 1
            return True
        else:
            print('Sorry this position has been carded')
            return False

    def show_grid_map(self):
        flag = 1
        num = 1
        cnt = 1
        print('Current mine state:')
        z = ['( '+ str(x) + ' )' for x in range(1,10)]
        show_list('     ',z)
        print('-----+'+ '-'*(self.w * 5 ))
        for i in self.grid_map:
            if num % 3  == 2 :
                show_list('( ' + str(flag) + ' )', i)
                flag += 1
            else:
                show_list('(   )', i)


            num +=1
            cnt +=1


class Path(Card):
    def __init__(self, usage='', n=True):
        super(Path, self).__init__()
        self.make_card(usage)
        # self.l = l
        # self.r = r
        # self.u = u
        # self.d = d
        self.n = n
        self.update_usage()
        # self.usage = '( {} )({}+{})( {} )'.format('|' if u else ' ', '-' if l else ' ', '-' if r else ' ', '|' if d else ' ')
    # def get_usage(self)/:
    def make_card(self, usage:str):
        usage = usage.upper()
        f =  lambda us: True if us.upper() in usage else False
        self.l = f('l')
        self.u = f('u')
        self.r = f('r')
        self.d = f('d')
        self.update_usage()

    def update_usage(self):
        self.usage = '( {} )({}+{})( {} )'.format('|' if self.u else ' ', '-' if self.l else ' ', '-' if self.r else ' ', '|' if self.d else ' ')


    def change_orientation(self):
        u = self.u
        d = self.d
        l = self.l
        r = self.r

        self.u = d
        self.d = u
        self.l = r
        self.r = l
        self.update_usage()

    def use(self):
        print('Do you need to change the orientation of this card?')
        bo = int(input('0 for no and 1 for yes'))
        try :
            bo = bool(bo)
        except:
            bo = bool(int(input('Please re-input whether to change the orientation , 0 for no and 1 for yes')))
        if bo :
            self.change_orientation()
        print('You have choose the card as behind')
        x, y = choose_position()
        flag = game.push_card(x, y, self)
        while not flag:
            x, y = choose_position('The position you choosed has been used, please re-choose your position to path')
            game.push_card(x, y, self)

        end = game.find_gold()
        return end
class Gold(Card):
    def __init__(self, value):
        super(Gold, self).__init__()
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        self.value += other.value
        return self

class Game:
    def __init__(self):
        self.map = Map()
        self.starting = Start()
        self.end = [End(gold=bool(x % 2)) for x in range(3)]
        self.players = [] # Player
        self.player_pointer = 0
        self.actor_list = []
        self.guys_num = 0
        self.cards = []
        self.cards_queue = deque()
        self.person_card_num = 0
        self.action_cards = []
        self.golds = deque()
        self.bad_players = []
        self.gold1 = deque()
        self.gold2 = deque()
        self.gold3 = deque()
        self.round = ['Round {}'.format(x) for x in range(3)]
        # self.welcome()

        for i in range(3):
            self.players.append(Player('name{}'.format(i), Actor(True)))
        self.get_card_num()
        self.make_gold()
        self.init_card()
        self.distribute_card()
        self.init_map()
        self.show()
        self.map.show_grid_map()
        # self.gaming()
    def make_gold(self):
        golds = [Gold(1) for x in range(16)]
        golds += [Gold(2) for x in range(8)]
        golds += [Gold(3) for x in range(4)]
        random.shuffle(golds)
        self.golds = deque(golds)

    def show_map_carded(self):
        self.map.show_grid()

    def find_gold(self):
        flag = 0
        for index, card in enumerate(self.end):
            if self.map.find_path(self.starting.y, self.starting.x, card.y, card.x):
                if card.found():
                    flag = 1
        return flag

    def show_end_card(self, x, y):
        print(self.end[int(x/2)])

    def get_player(self, index):
        return self.players[index]

    def show_card(self):
        for a, b in enumerate(self.players):
            print(a, b, b.cards)

    def get_gold(self) -> deque:
        # todo
        cards = deque()
        for i in self.players:
            cards.append(self.golds.popleft())
        return cards

    def distribute_gold(self, index, good:bool):
        index = index + len(self.players)
        player_size = len(self.players)

        golds = self.get_gold()

        for i in range(player_size * 2):
            player = self.players[index % player_size]
            if good:
                if player.is_good():
                    player.push_gold(golds.popleft())
            else:
                player.push_gold(golds.popleft())
            index -= 1
        print('Distribute golds finished')


    def good_distribution(self, index):
        self.distribute_gold(index, True)

    def bad_distribution(self, index):
        self.distribute_gold(index, False)

    def find_end(self):
        index = self.player_pointer + len(self.players)
        player_size = len(self.players)
        player = self.players[index % player_size]
        if player.is_good():
            self.good_distribution(index)
        else:
            self.bad_distribution(index)

    def gold_count(self):
        for i in self.golds:
            if str(i) == 1:
                self.gold1.append(Gold(1))
            elif str(i) == 2:
                self.gold2.append(Gold(2))
            else:
                self.gold3.append(Gold(3))

    def split_golds(self, golds):
        tmp = []
        if golds == 4:
            tmp = [(4, 0, 0), (2, 1, 0), (1, 0, 1), (0, 2, 0)]
        elif golds == 3:
            tmp = [(3, 0, 0), (1, 1, 0), (0, 0, 1)]
        else:
            tmp = [(2, 0, 0), (0, 1, 0)]
        return tmp

    def pop_golds(self, golds):
        self.gold_count()
        tmp = self.split_golds(golds)
        flag = False
        for i in tmp:
            if i[0] <= len(self.gold1) and i[1] <= len(self.gold2) and i[2] <= len(self.gold3):
                for j in range(i[0]):
                    self.golds.remove(self.gold1.pop())
                for j in range(i[1]):
                    self.golds.remove(self.gold2.pop())
                for j in range(i[2]):
                    self.golds.remove(self.gold3.pop())
                flag = True
                break
        if flag:
            return True
        else:
            return False

    def not_find_end(self):
        bad_guys = len(self.bad_players)
        golds = 0
        if bad_guys == 1:
            # todo use cards
            golds = 4
        elif bad_guys == 2 or 3:
            golds = 3
        else:
            golds = 2
        self.pop_golds(golds)

    def gaming(self):
        flag = False # to make sure whether the good or the bad
        for x in self.round:
            print('This is ' + x)
            for index, player in enumerate(self.players):
                card = player.choose()
                self.player_pointer = index
                if card is not None:
                    if card.use():
                        flag = True
                        self.find_end()
                        break

                cls()
                self.show()
                self.map.show_grid_map()
            if flag :
                continue
            else :
                self.not_find_end()
            self.show_card()



    def distribute_card(self):

        for player in self.players:
            # print(player)
            for i in range(self.person_card_num):
                card = self.cards_queue.popleft()
                # print(player,i, card)
                player.add_card(card)
            # print(player.cards)

        for player in self.players:
            print(player, player.cards, len(player.cards))

        print(len(self.cards_queue))

    def get_card_num(self):
        num = len(self.players)
        if num <= 5:
            self.person_card_num = 6
        elif num <=7:
            self.person_card_num = 5
        elif num <=10:
            self.person_card_num = 4

    def show_players(self):
        print('--------------------')
        # show_list_without('The {} players are:'.format(len(self.players)), self.players)
        for index, player in enumerate(self.players):
            print(index, end=' ')
            print(player, end=' ,')
    def init_card(self):
        # path
        self.cards = [Path('urdl') for x in range(5)] + [Path('urdl', n=False)]
        self.cards += [Path('urd') for x in range(5)] + [Path('urd', n=False)]
        self.cards += [Path('url') for x in range(5)] + [Path('url', n=False)]
        self.cards += [Path('ur') for x in range(5)] + [Path('ur', n=False)]
        self.cards += [Path('ul') for x in range(4)] + [Path('ul', n=False)]
        self.cards += [Path('ud') for x in range(4)] + [Path('ud', n=False)]
        self.cards += [Path('rl') for x in range(3)] + [Path('rl', n=False)]
        self.cards += [Path('u', n=False)]
        self.cards += [Path('r', n=False)]


        # tools
        self.action_cards += [Light() for x in range(2)] # L
        self.action_cards += [Pickaxe() for x in range(2)]  # P
        self.action_cards += [Cart() for x in range(2)] # W
        self.action_cards += [Broken_light() for x in range(3)]
        self.action_cards += [Broken_pickaxe() for x in range(3)]
        self.action_cards += [Broken_cart() for x in range(3)]
        self.action_cards += [Double_tool(True, True, False)]
        self.action_cards += [Double_tool(True, False, True)]
        self.action_cards += [Double_tool(False, True, True)]
        self.action_cards += [Tafang() for x in range(3)]
        self.action_cards += [Ditu() for x in range(6)]

        self.cards += self.action_cards
        random.shuffle(self.cards)
        self.cards_queue = deque(self.cards)

        print(len(self.cards))

    def push_card(self, x, y, card):
        # todo use return to make sure whether to push the card ,especially the path card
        return self.map.push_card(x, y, card)

    def init_map(self):
        self.push_card(3, 1, self.starting)
        self.starting.change_position(get_x(3), get_y(1))
        for a,b in zip([1,3,5], self.end):
            self.push_card(a, 9, b)
            b.change_position(get_x(a), get_y(9))
        # self.push_card(3, 2, Path())



    def show(self):
        self.map.show()

    def add_player(self):
        cnt = len(self.players)
        inp = input('Please enter the name of player {} and its status(AI: 0,Human:1):'.format(cnt))
        name, status = inp.split(',')
        name = name.strip()
        status = int(status.strip())
        if status:
            cls()
            print('\ryour actor is {}'.format('good' if self.actor_list[cnt].is_good() else 'bad'), end='')
            input(' ,please enter to pass')
            cls()
        player = Player(name, self.actor_list[cnt], status)
        self.players.append(player)
        self.bad_players.append(player)


    def welcome(self):
        print('+-----------------------------------------------------------------+')
        print('|Welcome to Sabootters,where dwarf otters look for gold in a mine!|')
        print('+-----------------------------------------------------------------+')
        num = int(input('How many players?'))
        self.guys_num = num
        self.make_actor_list()
        for x in range(num):
            self.add_player()
        print('--------------------')
        show_list_without('The {} players are:'.format(len(self.players)), self.players)
        input('enter to go achead')

    def person_list_generate(self, good, bad):
        person_list = [Actor(True) for x in range(good)]
        person_list += [Actor(False) for y in range(bad)]
        return  person_list

    def make_actor_list(self):
        """
        process the person_list and generate a list which stands for who is good airen
        :return: a list
        """
        num = self.guys_num
        good = 0
        bad = 0
        if num == 3:
            good = 3
        elif num==4 or num == 5:
            good =4
        elif num == 6 or num == 7:
            good = 5
        elif num == 8 :
            good = 6
        elif num == 9:
            good = 7
        elif num == 10 :
            good = 7
        bad = num + 1 - good
        person_list = self.person_list_generate(good, bad)
        random.shuffle(person_list)
        self.actor_list = person_list[:-1]
        print(self.actor_list)

game = Game()


if __name__=='__main__':
    # todo: 1. three lines
    # todo: 2. gui
    # todo: 3. play
    # todo: 4. gold card
    #
    # game.show()/
    #
    # card = Start()
    # card = Broken_cart().show()
    # game.gaming()
    # game.show_map_carded()
    # path = Path('url')
    # print(path)
    # path.change_orientation()
    # print(path)
    game.gold_count()
    # path = Path('urdl')
    # game.push_card(3,2, path)
    # game.push_card(2,2, path)
    # game.push_card(2,3, path)
    # game.push_card(2,4, path)
    # game.push_card(2,5, path)
    # game.push_card(2,6, path)
    # game.push_card(2,7, path)
    # game.push_card(2,8, path)
    # game.push_card(2,9, path)
    # print(game.find_gold())
    # game.show()

    # print(get_x(3), get_y(1))