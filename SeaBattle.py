from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы пытаетесь выстрелить за пределы доски!'

class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку!'

class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'

class Ship:
    def __init__(self, length, bow, orientation):
        self.length = length
        self.bow = bow
        self.orientation = orientation
        self.health = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cor_x = self.bow.x
            cor_y = self.bow.y
            if self.orientation == 0:
                cor_x += i
            elif self.orientation == 1:
                cor_y += i
            ship_dots.append(Dot(cor_x, cor_y))
        return ship_dots

    def shooten(self, shoot):
        return shoot in self.dots()

class Board:

    def __init__(self, hid=False):
        self.hid = hid
        self.alive_ships = []
        self.list_dots = [['O'] * 6 for _ in range(6)]
        self.busy = []
        self.count = 0

    def __str__(self):

        board = '    | 0 | 1 | 2 | 3 | 4 | 5 |'
        for i, row in enumerate(self.list_dots):
            board += f'\n| {i} | ' + ' | '.join(row) + ' |'
        if self.hid:
            board = board.replace('♦', 'O')
        return board


    def out(self, d):
        return not ((0 <= d.x <= 5) and (0 <= d.y <= 5))

    def contour(self, ship):
        con = [(-1, 1), (0, 1), (1, 1),
               (-1, 0), (0, 0), (1, 0),
               (-1, -1), (0, -1), (1, -1)
               ]
        for i in ship.dots:
            for dx, dy in con:
                cor = Dot(i.x + dx, i.y + dy)
                self.busy.append(cor)


    def add_ship(self, ship):
        for i in ship.dots:
            if self.out(i) or i in self.busy:
                raise BoardWrongShipException()
        for i in ship.dots:
            self.list_dots[i.x][i.y] = '♦'
            self.busy.append(i)
        self.alive_ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            return BoardOutException()
        if d in self.busy:
            return BoardUsedException()

        self.busy.append(d)

        for ship in self.alive_ships:
            if d in ship.dots:
                ship.health -= 1
                self.list_dots[d.x][d.y] = 'X'
                if ship.health == 0:
                    self.count += 1
                    print('Корабль поражен!')
                    return False
                else:
                    print('Попадание по кораблю!')
                    return True
        self.list_dots[d.x][d.y] = '-'
        print('Промах!')
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, self_b, other_b):
        self.self_b = self_b
        self.other_b = other_b

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.other_b.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):

    def ask(self):
        target = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {target.x}, {target.y}')
        return target

class User(Player):

    def ask(self):
        while True:
            target = input('Введите координаты выстрела: ')
            if all(i == ' ' for i in list(target)):
                print('Вы ничего не ввели!')
                continue
            elif ' ' in list(target):
                target = target.split()
            else:
                target = list(target)
            try:
                target = list(map(int, target))
            except ValueError:
                print('Вы ввели не числа!')
                continue
            if target[0] > 9 or target[1] > 9:
                print('У вас что-то не в порядке с координатами...')
                continue
            elif len(target) != 2:
                print('Слишком много координат...')
                continue
            x, y = target
            return Dot(x, y)

class Game:
    def __init__(self):
        player = self.random_board()
        computer = self.random_board()
        computer.hid = True

        self.ai = AI(computer, player)
        self.us = User(player, computer)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        count = 0
        for l in lens:
            while True:
                count += 1
                if count >= 2000:
                    return None
                ship = Ship(l, Dot(randint(0, 5), randint(0, 5)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print('-'*20)
            print('Доска игрока:')
            print(self.us.self_b)
            print('-' * 20)
            print('Доска компьютера:')
            print(self.ai.self_b)
            if num % 2 == 0:
                print('Ход игрока:')
                repeat = self.us.move()
            else:
                print('Ход компьютера:')
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.self_b.count == 7:
                print('-'*20)
                print('Пользователь победил!')
                break
            if self.us.self_b.count == 7:
                print('-'*20)
                print('Компьютер победил!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()



game = Game()
print(game.start())