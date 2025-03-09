# Импортируем модуль turtle для создания графического интерфейса
from turtle import *
# Импортируем модуль time для работы со временем
import time

# Устанавливаем ширину игрового поля
s_width = 200
# Устанавливаем высоту игрового поля
s_height = 200

# Создаем базовый класс Sprite, наследующийся от класса Turtle
class Sprite(Turtle):
    # Инициализируем спрайт с параметрами: координаты, шаг, форма, цвет и множитель скорости
    def __init__(self, x, y, step=10, shape='turtle', color='orange', speed_mult=50):
        # Вызываем конструктор родительского класса
        super().__init__()
        # Поднимаем перо (чтобы не рисовать линии при движении)
        self.penup()
        # Устанавливаем максимальную скорость анимации
        self.speed(0)
        # Перемещаем спрайт в указанные координаты
        self.goto(x, y)
        # Устанавливаем цвет спрайта
        self.color(color)
        # Устанавливаем форму спрайта
        self.shape(shape)
        # Устанавливаем размер шага
        self.step = step
        # Устанавливаем множитель скорости
        self.speed_mult = speed_mult
        # Устанавливаем направление движения (1 или -1)
        self.direction = 1
        # Инициализируем счетчик очков
        self.points = 0

    # Метод для движения вверх
    def move_up(self):
        # Увеличиваем y-координату на величину шага
        self.sety(self.ycor() + self.step)

    # Метод для движения вниз
    def move_down(self):
        # Уменьшаем y-координату на величину шага
        self.sety(self.ycor() - self.step)

    # Метод для движения влево
    def move_left(self):
        # Уменьшаем x-координату на величину шага
        self.setx(self.xcor() - self.step)

    # Метод для движения вправо
    def move_right(self):
        # Увеличиваем x-координату на величину шага
        self.setx(self.xcor() + self.step)

    # Метод проверки столкновения с другим спрайтом
    def is_collide(self, sprite):
        # Возвращает True, если расстояние между спрайтами меньше 20
        return self.distance(sprite.xcor(), sprite.ycor()) < 20

# Создаем класс Enemy, наследующийся от Sprite
class Enemy(Sprite):
    # Инициализируем врага с дополнительным параметром начального направления
    def __init__(self, x, y, step=10, shape='cicle', color='orange', speed_mult=50, start_direction=1):
        # Вызываем конструктор родительского класса
        super().__init__(x, y, step, shape, color, speed_mult)
        # Устанавливаем начальное направление движения
        self.direction = start_direction

    # Метод установки параметров движения
    def set_move(self, x_start, y_start, x_end, y_end):
        # Устанавливаем начальные и конечные координаты движения
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end

        # Определяем начальную x-координату в зависимости от направления
        if self.direction == -1:
            start_x = x_end
        else:
            start_x = x_start
        # Перемещаем врага в начальную позицию
        self.goto(start_x, y_start)

    # Метод выполнения шага движения
    def make_step(self):
        # Вычисляем новую x-координату
        new_x = self.xcor() + (self.step * self.speed_mult * self.direction)
        # Устанавливаем новую x-координату
        self.setx(new_x)

        # Если достигнута граница движения, меняем направление
        if new_x >= self.x_end or new_x <= self.x_start:
            self.direction *= -1

# Создаем класс Goal (цель), наследующийся от Sprite
class Goal(Sprite):
    # Метод установки параметров движения
    def set_move(self, x_start, y_start, x_end, y_end):
        # Устанавливаем начальные и конечные координаты движения
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        # Перемещаемся в начальную позицию
        self.goto(x_start, y_start)
        # Поворачиваемся к конечной точке
        self.setheading(self.towards(x_end, y_end))

    # Метод выполнения шага движения
    def make_step(self):
        # Двигаемся вперед на заданное расстояние
        self.forward(self.step * self.speed_mult)

        # Если достигнута конечная точка
        if self.distance(self.x_end, self.y_end) < self.step * self.speed_mult:
            # Меняем местами начальную и конечную точки
            temp_x = self.x_end
            temp_y = self.y_end
            self.x_end = self.x_start
            self.y_end = self.y_start
            self.x_start = temp_x
            self.y_start = temp_y
            # Поворачиваемся к новой конечной точке
            self.setheading(self.towards(self.x_end, self.y_end))   

# Создаем игрока в начальной позиции
player = Sprite(0, -150)

# Создаем первого врага
enemy1 = Enemy(-s_width, 0, 0.1, 'square', color='red', speed_mult=50, start_direction=1)
# Устанавливаем параметры движения первого врага
enemy1.set_move(-s_width, 0, s_width, 0)

# Создаем второго врага
enemy2 = Enemy(-s_width, 70, 0.11, 'square', 'red', speed_mult=50, start_direction=-1)
# Устанавливаем параметры движения второго врага
enemy2.set_move(-s_width, 70, s_width, 70)    

# Создаем третьего врага
enemy3 = Enemy(-s_width, -70, 0.12, 'square', 'red', speed_mult=50, start_direction=1)
# Устанавливаем параметры движения третьего врага
enemy3.set_move(-s_width, -70, s_width, 0)

# Создаем четвертого врага
enemy4 = Enemy(-s_width, 140, 0.09, 'square', 'red', speed_mult=50, start_direction=-1)
# Устанавливаем параметры движения четвертого врага
enemy4.set_move(-s_width, 140, s_width, 0)

# Создаем цель
goal = Goal(-s_width, 200, 0.1, 'triangle', 'green', speed_mult=50)
# Устанавливаем параметры движения цели
goal.set_move(-s_width, s_height, s_width, s_height)

# Создаем список всех врагов
enemies = [enemy1, enemy2, enemy3, enemy4]

# Создаем экран
scr = Screen()
# Отключаем автоматическое обновление экрана
scr.tracer(0)
# Включаем прослушивание событий клавиатуры
scr.listen()
# Привязываем клавиши управления к методам движения игрока
scr.onkey(player.move_up, 'Up')
scr.onkey(player.move_down, 'Down')
# Флаг окончания игры
game_over = False
# Запрашиваем у пользователя количество очков для победы
score_to_win = 5
# score_to_win = int(input("Введите количество очков для победы:"))
# Запоминаем время начала игры
start_time = time.time()

# Функция завершения игры
def end_game(string):
    # Используем глобальную переменную game_over
    global game_over
    # Устанавливаем флаг окончания игры
    game_over = True
    # Скрываем игрока и цель
    for sprite in [player, goal]:
        sprite.hideturtle()
    # Скрываем всех врагов
    for enemy in enemies:
        enemy.hideturtle()
    # Обновляем экран
    scr.update()
    # Вычисляем время игры
    game_time = round((time.time() - start_time), 2)
    # Перемещаем цель для вывода текста
    goal.goto(-150, 0)
    # Меняем цвет текста на черный
    goal.color('black')
    # Формируем строку с временем игры
    full_string = 'Время игры:' + str(game_time) + ' сек'
    # Выводим результат игры
    goal.write(string, font=('Arial', 30, 'bold'))
    # Перемещаем цель для вывода времени
    goal.goto(-150, -50)
    # Выводим время игры
    goal.write(full_string, font=('Arial', 30, 'bold'))
    # Обновляем экран
    scr.update()

# Функция обновления игры
def update():
    # Используем глобальную переменную game_over
    global game_over
    # Если игра окончена, выходим из функции
    if game_over: return
    # Двигаем всех врагов
    for enemy in enemies:
        enemy.make_step()
    # Двигаем цель
    goal.make_step()
    # Проверяем столкновение игрока с целью
    if player.is_collide(goal):
        # Увеличиваем счет
        player.points += 1
        # Возвращаем игрока на начальную позицию
        player.goto(0, -150)
    # Проверяем столкновение игрока с врагами
    for enemy in enemies:
        if player.is_collide(enemy):
            # Завершаем игру поражением
            end_game('You lose')
            return
    # Используем глобальную переменную score_to_win
    global score_to_win
    # Проверяем достижение необходимого количества очков
    if player.points >= score_to_win:
        # Завершаем игру победой
        end_game('You win')
        return
    # Обновляем экран
    scr.update()
    # Планируем следующее обновление через 10 миллисекунд
    scr.ontimer(update, 10)
# Запускаем первое обновление игры
update()
# Запускаем главный цикл игры
scr.mainloop()