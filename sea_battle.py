def __init__(self, size=6):
    self.size = size
    pl = self.random_board()
    co = self.random_board()
    co.hid = True

    self.ai = AI(co, pl)
    self.us = User(pl, co)

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
        print("-" * 20)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 20)
        print("Доска компьютера:")
        print(self.ai.board)
        print("-" * 20)
        if num % 2 == 0:
            print("Ходит пользователь!")
            repeat = self.us.move()
        else:
            print("Ходит компьютер!")
            repeat = self.ai.move()
        if repeat:
            num -= 1

        if self.ai.board.count == 7:
            print("-" * 20)
            print("Пользователь выиграл!")
            break

        if self.us.board.count == 7:
            print("-" * 20)
            print("Компьютер выиграл!")
            break
        num += 1

def start(self):
    self.greet()
    self.loop()

#print (Pointer.__doc__)
#print (Exception.__doc__)
#print (PlayingFieldException.__doc__)
#print (PlayingFieldOutException.__doc__)
#g = Game()
#g.start()