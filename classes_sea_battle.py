class PlayingFieldException(Exception):
    """
Класс PlayingFieldException -
        класс исключения для игрового поля дочерний общему базовому классу Exception
    """
    pass

class PlayingFieldOutException(PlayingFieldException):
    """
Класс PlayingFieldOutException -
        класс исключения для события выхода за пределы игрового поля
    """
    def __str__(self):        # магический метод  __str__ возвращает строку для события выхода за пределы игрового поля
        return "Выстрел за пределы поля!"

class PlayingFieldUsedException(PlayingFieldException):
    """
Класс PlayingFieldUsedException -
        класс исключения для события повторного выстрела в клетку игрового поля
    """
    def __str__(self):       # магический метод  __str__ возвращает строку для события повторного выстрела в клетку игрового поля
        return "В эту клетку уже стреляли!"

class PlayingFieldWrongShipException(PlayingFieldException):
    """
Класс PlayingFieldWrongShip -
            класс исключения для события выхода за пределы игрового поля
    """
    pass

class Pointer:
    """
Класс Pointer -
       класс объекта точка.
       Каждая точка описывается свойствами:
       - координата по оси x
       - координата по оси y
    """
    def __init__(self, x, y):   # магические метод __init__ для начальной инициализации класса Pointer
        self.x = x              # координата по оси x
        self.y = y              # координата по оси y

    def __eq__(self, other):    # метод __eq__ проверяет равенство точек
        return self.x == other.x and self.y == other.y

    def __repr__(self):         # магический метод __repr__ возвращает представление объета (точки)
        return f"Pointer({self.x}, {self.y})"

class Ship:
    """
Класс Ship - класс объекта корабль для игры "Морской бой"
        Каждый корабль описывается свойствами:
        - палубность (1 - 4)
        - расположение (0 - горизонтальное, 1 - вертикальное)
        - ключевая точка расположения носа коробля (тег в формате: "столбец_строка")
        - массив со статусами точек, который формируется конструктором
        - массив с координатами точек корабля, который формируется конструктором
        - координаты точек вокруг корабля
        - статус гибели корабля
        - префикс тега (для своих кораблей будет, например, "my", для чужих "nmy"
        Каждый корабль описывается следующими методами:
        - изменение массива жизней коробля со статусами точек, например [0,0,1,0]
        - shoot(координаты точки), возвращает 1 - если попали, 2 - убил, 0 - мимо
    """
    def __init__(self, bow, l, o):  # магические метод __init__ для начальной инициализации класса Ship
        self.bow = bow # расположение
        self.l = l # палубность
        self.o = o #ключевая точка
        self.lives = l  #жизни

    @property
    def points(self): # метод возвращает все точки корабля
        ship_points = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_points.append(Pointer(cur_x, cur_y))

        return ship_points

    def shooten(self, shot):
        return shot in self.points

class Board:
    """
Класс Board - класс объекта игровое поле для игры "Морской бой"
        Описывается свойствами:
        - двумерный список, в котором хранятся состояния каждой клетки
        - список кораблей
        - параметр hid типа bool - информация о том, нужно ли скрывать корабли на
        доске(для вывода доски врага), или нет (для своей доски).
        - колличество живых кораблей на доске
        Описывается следующими методами:
        - метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключение)
        - метод counter, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке
        кораблей (помечает соседние точки, где корабля по правилам быть не может).
        - метод out, который для точки (объекта класса Pointer) возвращает True, если точка выходит за пределы поля,
        и False, если не выходит.
        - метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку,
         нужно выбрасывать исключения).
    """
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class Player:
    """
класс Player - класс игрока в игру.
    описывается свойствами:
    - собственная доска (объект класса Board)
    - доска врага
    имеются следующие методы:
    - ask - метод, который "спрашивает" игрока, в какую клетку он делает выстрел
    - move - метод, который делает ход в игре. Тут мы вызываем метод ask,
    """
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:

                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class Game:
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
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