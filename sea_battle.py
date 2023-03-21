from random import randint  # подключаем из  модуля random (генерация случайных чисел) метод randint

class Ship:
    """
Класс Ship - класс объекта корабль для игры "Морской бой"
        Каждый корабль описывается свойствами:
        - ключевая точка расположения носа коробля
        - длина коробля (1 - 3)
        - расположение (0 - горизонтальное, 1 - вертикальное)
        - жизни корабля (= длина корабля)
        Каждый корабль описывается следующими методами:
        - методом возвращающим все точки корабля

    """
    def __init__(self, key_point, ship_length, orientation):  # магические метод __init__ для начальной инициализации класса Ship
        self.key_point = key_point                            # ключевая точка расположения носа коробля
        self.ship_length = ship_length                        # длина коробля
        self.orientation = orientation                        # расположение (0 - горизонтальное, 1 - вертикальное)
        self.lives = ship_length                              # жизни корабля (= длина корабля)

    @property
    def points(self):                                         # метод возвращает все точки корабля
        ship_points = []                                      # начальное значение
        for i in range(self.ship_length):
            ship_x = self.key_point.x
            ship_y = self.key_point.y
            if self.orientation == 0:                         # проверяем расположение 0 - горизонтальное
                ship_x += i
            elif self.orientation == 1:                       # проверяем расположение 1 - вертикальное
                ship_y += i
            ship_points.append(Pointer(ship_x, ship_y))       # добавляем точки в кораблик
        return ship_points                                    # возвращаем значение точек корабля

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
        return "Перелёт! Стреляй точнее!"

class PlayingFieldUsedException(PlayingFieldException):
    """
Класс PlayingFieldUsedException -
        класс исключения для события повторного выстрела в клетку игрового поля
    """
    def __str__(self):       # магический метод  __str__ возвращает строку для события повторного выстрела в клетку игрового поля
        return "Повторный выстрел в одну клетку!"

class PlayingFieldWrongShipException(PlayingFieldException):
    """
Класс PlayingFieldWrongShip -
            класс исключения для события положения кораблика
    """
    pass

class PlayingField:
    """
Класс PlayingField - класс объекта игровое поле для игры "Морской бой"
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
    def __init__(self, hid=False, size=6):                # магические метод __init__ для начальной инициализации класса игрового поля
        self.size = size                                  # размер поля
        self.hid = hid                                    # видимость кораблика на поле
        self.count = 0                                    # количество подбитых корабликов
        self.field = [["O"] * size for _ in range(size)]  # создание поля
        self.busy = []                                    # лист занятых точек
        self.ships = []                                   # лист точек кораблей

    def prinfield(self, other):   # метод заполнение поля занятых точек
        res = "-------------------------------------------------------------- \n"
        res += "          Поле Игрока                 Поле Компьютера          \n"
        res += "-------------------------------------------------------------- \n"
        res += "  || 1 | 2 | 3 | 4 | 5 | 6 ||   || 1 | 2 | 3 | 4 | 5 | 6 || "
        for i in range(6):                                     # цикл для обхода поля
            res += "\n" + str(i + 1) + " ||"
            for j in range(6):                                 # цикл для поля игрока
                line = str()
                line += " " + self.field[i][j] + " |"          # строка поля игрока
                if self.hid:
                    line = line.replace("■", "O")              # проверяем отображение кораблей на поле
                res += line
            res += "|   ||"                                    # добавляем разделитель

            for j in range(6):                                 # цикл для поля компьютера
                line = str()
                line += " " + other.field[i][j] + " |"         # строка поля компьютера
                if other.hid:
                    line = line.replace("■", "O")              # проверяем отображение кораблей на поле
                res += line
            res += "| " + str(i + 1)                           # добавляем нумерацию

        return res
    def out(self, d):                                          # метод проверки выхода за пределы поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))
    def contour(self, ship, verb=False):                       # метод контур кораблика
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.points:
            for dx, dy in near:
                cur = Pointer(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
    def add_ship(self, ship):                             # добавление кораблика на поле
        for d in ship.points:
            if self.out(d) or d in self.busy:             # проверка ошибки расположения кораблика
                raise PlayingFieldWrongShipException()
        for d in ship.points:                             # добавление кораблика на поле
            self.field[d.x][d.y] = "■"                    # заполнение поля
            self.busy.append(d)                           # добавление координат в поле занятых клето

        self.ships.append(ship)                           # добавление кораблика в массив точек кораблей
        self.contour(ship)                                # оконтовка кораблика

    def shot(self, d):                                    # выстрел
        if self.out(d):                                   # проверка ошибки поля
            raise PlayingFieldOutException()
        if d in self.busy:                                # проверка ошибки поля
            raise PlayingFieldUsedException()
        self.busy.append(d)                               # добавление точки в поле занятых клеток
        for ship in self.ships:                           # проход по кораблику
            if d in ship.points:                            # если точка в кораблике
                ship.lives -= 1                           # минус жизнь
                self.field[d.x][d.y] = "X"                # заполнение поля
                if ship.lives == 0:                       # если жизней у кораблика нет
                    self.count += 1                       # обновление счетчика подбитых кораблей
                    self.contour(ship, verb=True)         # создание контура бодбитого кораблика
                    print("Корабль уничтожен!")
                    return False                          # при уничкожении кораблика + ход
                else:
                    print("Корабль ранен!")
                    return True                           # при подбитии кораблика + ход

        self.field[d.x][d.y] = "."                        # заполнение поля промахом
        print("Мимо!")
        return False                                      # нет дополнительного хода

    def begin(self):                                      # обновления поля занятых точек
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
        self.board = board                               # своё поле
        self.enemy = enemy                               # поле врага

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try: # отлов ошибок
                target = self.ask()                      # запрос точки
                repeat = self.enemy.shot(target)         # выстрел по запрошенной точке
                return repeat
            except PlayingFieldException as e:
                print(e)

class Game: # класс игра
    def try_board(self):                                  # добавление на доску кораблей
        lens = [3, 2, 2, 1, 1, 1, 1]                      # список длин корабликов
        board = PlayingField(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Pointer(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except PlayingFieldWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):                               # создание рандомной доски
        board = None
        while board is None:
            board = self.try_board()
        return board

    def __init__(self, size=6):
        self.size = size                                  # задание размера поля
        pl = self.random_board()                          # поле игрока
        co = self.random_board()                          # поле компьютера
        co.hid = True                                     # отображение корабли
        self.comp = Comp(co, pl)                            # определяем поле для компьютера
        self.user = User(pl, co)                            # определяем поле для пользователя

    def greet(self):                                      # приветствие
        print("-------------------")
        print("  \"Морской бой\"  ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):                                            # метод основного цикла игры
        num = 0                                                # задаем начальное значение счетчика ходов
        while True:                                            # запускаем цикл
            print("-" * 20)                                    # выводим разделитель
            print(self.user.board.prinfield(self.comp.board))  # выводим поле игроков в консоль
            print("-" * 20)                                    # выводим разделитель
            if num % 2 == 0:                                   # определяем ход для игрока
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:                                              # иначе ход компьютера
                print("Ходит компьютер!")
                repeat = self.comp.move()
            if repeat:
                num -= 1
            if self.comp.board.count == 7:                     # условие победы для пользователя
                print("-" * 20)
                print("Пользователь выиграл!")
                break
            if self.user.board.count == 7:                     # условие победы для компьютера
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def run(self):                                        # метод для запуска игры
        self.greet()                                      # выводим заставку
        self.loop()                                       # запускаем основной цикл игры

class User(Player):  # ход игрока
    """
класс User(Player) - класс хода игрока.
    описывается следующим методом:
    - ask - метод, запрашивает координаты точки из консоли
    """
    def ask(self):
        while True:                                         # запрашиваем координаты точки из консоли
            cords_point = input("Ваш ход: ").split()
            if len(cords_point) != 2:
                print(" Введите 2 координаты! ")
                continue
            x, y = cords_point
            if not (x.isdigit()) or not (y.isdigit()):      # проверяем, что с консоли вводили только цифры
                print(" Введите числа! ")
                continue
            x, y = int(x), int(y)
            return Pointer(x - 1, y - 1)

class Comp(Player):
    """
класс Comp(Player) - класс хода комптютера.
    описывается следующим методом:
    - ask - метод, случайным образом возвращает координаты хода компьютера с помощью метода randint
    """
    def ask(self):
        comp = Pointer (randint(0, 5), randint(0, 5))        # получаем координаты для хода компьютера
        print(f"Ход компьютера: {comp.x + 1} {comp.y + 1}")  # печатаем координаты в консоль
        return comp


sea_battle = Game()  # создаем экземпляр класса Game
sea_battle.run()     # запускаем для него метод run