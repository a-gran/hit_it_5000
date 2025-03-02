# Импортируем все классы и функции из модуля turtle для создания графики
from turtle import *
# Импортируем модуль time для работы со временем
import time

# Определяем константы размеров игрового поля
s_width = 200    # Ширина поля в пикселях
s_height = 200   # Высота поля в пикселях

# Базовый класс для всех объектов игры, наследуется от класса Turtle
class Sprite(Turtle):
    def __init__(self, x, y, step=10, shape='circle', color='orange', speed_mult=50):
        super().__init__()                # Вызываем конструктор родительского класса
        self.penup()                      # Поднимаем перо, чтобы не оставлять след при движении
        self.goto(x, y)                   # Перемещаем объект в начальную позицию
        self.color(color)                 # Устанавливаем цвет объекта
        self.shape(shape)                 # Устанавливаем форму объекта
        self.step = step                  # Устанавливаем размер шага
        self.speed(0)                     # Устанавливаем максимальную скорость анимации
        self.speed_multiplier = speed_mult  # Устанавливаем множитель скорости
        self.direction = 1                # Устанавливаем начальное направление (1 - вправо)
        self.points = 0                   # Инициализируем счетчик очков

    # Метод для движения вверх
    def move_up(self):
        self.sety(self.ycor() + self.step)    # Увеличиваем y-координату на величину шага

    # Метод для движения вниз
    def move_down(self):
        self.sety(self.ycor() - self.step)    # Уменьшаем y-координату на величину шага

    # Метод для движения влево
    def move_left(self):
        self.setx(self.xcor() - self.step)    # Уменьшаем x-координату на величину шага

    # Метод для движения вправо
    def move_right(self):
        self.setx(self.xcor() + self.step)    # Увеличиваем x-координату на величину шага

    # Метод проверки столкновения с другим спрайтом
    def is_collide(self, sprite):
        # Возвращаем True, если расстояние между объектами меньше 20
        return self.distance(sprite.xcor(), sprite.ycor()) < 20

# Класс врага, наследуется от Sprite
class Enemy(Sprite):
    def __init__(self, x, y, step=10, shape='circle', color='orange', speed_mult=50, start_direction=1):
        # Вызываем конструктор родительского класса с переданными параметрами
        super().__init__(x, y, step, shape, color, speed_mult)
        self.direction = start_direction  # Устанавливаем начальное направление движения

    # Метод установки границ движения
    def set_move(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start          # Устанавливаем начальную X координату
        self.y_start = y_start          # Устанавливаем начальную Y координату
        self.x_end = x_end              # Устанавливаем конечную X координату
        self.y_end = y_end              # Устанавливаем конечную Y координату
        
        # Определяем начальную позицию в зависимости от направления движения
        if self.direction == -1:        # Если движение влево
            start_x = x_end             # Начинаем с правого края
        else:                           # Если движение вправо
            start_x = x_start           # Начинаем с левого края
        self.goto(start_x, y_start)     # Перемещаем врага в начальную позицию

    # Метод выполнения шага движения
    def make_step(self):
        # Вычисляем новую позицию с учетом направления и скорости
        new_x = self.xcor() + (self.step * self.speed_multiplier * self.direction)
        self.setx(new_x)                # Устанавливаем новую X координату
        
        # Если достигли границы, меняем направление движения
        if new_x >= self.x_end or new_x <= self.x_start:
            self.direction *= -1        # Меняем направление на противоположное

# Класс цели, наследуется от Sprite
class Goal(Sprite):
    # Метод выполнения шага движения
    def make_step(self):
        # Двигаемся вперед с учетом скорости
        self.forward(self.step * self.speed_multiplier)
        
        # Проверяем, достигли ли конечной точки
        if self.distance(self.x_end, self.y_end) < self.step * self.speed_multiplier:
            # Меняем местами начальную и конечную точки
            temp_x = self.x_end
            temp_y = self.y_end
            self.x_end = self.x_start
            self.y_end = self.y_start
            self.x_start = temp_x
            self.y_start = temp_y
            # Поворачиваемся к новой цели
            self.setheading(self.towards(self.x_end, self.y_end))

    # Метод установки границ движения
    def set_move(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start          # Устанавливаем начальную X координату
        self.y_start = y_start          # Устанавливаем начальную Y координату
        self.x_end = x_end              # Устанавливаем конечную X координату
        self.y_end = y_end              # Устанавливаем конечную Y координату
        self.goto(x_start, y_start)     # Перемещаем цель в начальную позицию
        # Поворачиваемся в направлении конечной точки
        self.setheading(self.towards(x_end, y_end))

# Основной класс игры, управляющий всей логикой
class Game:
    def __init__(self):
        # Инициализация основных переменных игры
        self.score_to_win = 0           # Количество очков для победы
        self.game_started = False       # Флаг начала игры
        self.game_over = False          # Флаг окончания игры
        self.start_time = 0             # Время начала игры
        self.current_input = ""         # Текущий ввод пользователя в поле ввода
        
        # Создание и настройка игрового окна
        self.screen = Screen()          # Создаем экран
        self.screen.setup(800, 600)     # Устанавливаем размер окна
        self.screen.tracer(0)           # Отключаем автоматическое обновление экрана
        
        # Создание объекта для отображения текста
        self.text_display = Turtle()     # Создаем черепашку для текста
        self.text_display.hideturtle()   # Скрываем её
        self.text_display.penup()        # Поднимаем перо
        
        # Создание объекта для отображения поля ввода
        self.input_box = Turtle()        # Создаем черепашку для поля ввода
        self.input_box.hideturtle()      # Скрываем её
        self.input_box.penup()           # Поднимаем перо
        
        # Создаем все игровые объекты
        self.create_game_objects()       
        # Скрываем их до начала игры
        self.hide_game_objects()
        
        # Настройка обработчиков событий клавиатуры
        self.screen.listen()             # Включаем прослушивание клавиатуры
        # Привязываем обработчики для всех цифр
        for i in range(10):
            self.screen.onkey(lambda i=i: self.handle_number(str(i)), str(i))
        # Привязываем обработчики для специальных клавиш
        self.screen.onkey(self.handle_backspace, "BackSpace")
        self.screen.onkey(self.handle_enter, "Return")

    # Метод создания всех игровых объектов
    def create_game_objects(self):
        # Создаем игрока
        self.player = Sprite(0, -150, step=10, shape='turtle', color='purple')
        self.player.left(90)    # Поворачиваем игрока вверх

        # Создаем первого врага
        self.enemy1 = Enemy(-s_width, 0, step=0.1, shape='square', color='red', 
                           speed_mult=40, start_direction=1)
        self.enemy1.set_move(-s_width, 0, s_width, 0)

        # Создаем второго врага
        self.enemy2 = Enemy(-s_width, 70, step=0.1, shape='square', color='red', 
                           speed_mult=60, start_direction=-1)
        self.enemy2.set_move(-s_width, 70, s_width, 70)

        # Создаем третьего врага
        self.enemy3 = Enemy(-s_width, -70, step=0.1, shape='square', color='red', 
                           speed_mult=30, start_direction=1)
        self.enemy3.set_move(-s_width, -70, s_width, -70)

        # Создаем четвертого врага
        self.enemy4 = Enemy(-s_width, 140, step=0.1, shape='square', color='red', 
                           speed_mult=50, start_direction=-1)
        self.enemy4.set_move(-s_width, 140, s_width, 140)

        # Создаем цель
        self.goal = Goal(-s_width, 200, step=0.1, shape='triangle', color='green', 
                        speed_mult=50)
        self.goal.set_move(-s_width, s_height, s_width, s_height)

        # Создаем список всех врагов для удобства управления
        self.enemies = [self.enemy1, self.enemy2, self.enemy3, self.enemy4]

    # Метод скрытия всех игровых объектов
    def hide_game_objects(self):
        self.player.hideturtle()        # Скрываем игрока
        for enemy in self.enemies:      # Скрываем всех врагов
            enemy.hideturtle()
        self.goal.hideturtle()          # Скрываем цель

    # Метод показа всех игровых объектов
    def show_game_objects(self):
        self.player.showturtle()        # Показываем игрока
        for enemy in self.enemies:      # Показываем всех врагов
            enemy.showturtle()
        self.goal.showturtle()          # Показываем цель

    # Метод отрисовки поля ввода очков
    def draw_input_box(self):
        # Очищаем предыдущее состояние
        self.text_display.clear()
        self.input_box.clear()
        
        # Рисуем заголовок
        self.text_display.goto(0, 100)
        self.text_display.write("Введите количество очков для победы (1-20):",
                            align="center", font=('Arial', 20, 'normal'))
        
        # Рисуем прямоугольное поле ввода
        self.input_box.penup()
        self.input_box.color('black')
        
        # Увеличиваем размер поля для лучшего отображения
        box_width = 70   # Ширина поля
        box_height = 50   # Высота поля
        
        # Вычисляем координаты левого верхнего угла,
        # чтобы прямоугольник был отцентрирован
        start_x = -box_width // 2
        start_y = 30
        
        # Перемещаемся в начальную позицию и начинаем рисовать
        self.input_box.goto(start_x, start_y)
        self.input_box.pendown()
        
        # Рисуем прямоугольник
        for _ in range(2):
            self.input_box.forward(box_width)   # ширина поля
            self.input_box.right(90)
            self.input_box.forward(box_height)  # высота поля
            self.input_box.right(90)

        # ВТОРАЯ ЧАСТЬ НОВОГО КОДА - ОТОБРАЖЕНИЕ ТЕКСТА
        # Рисуем курсор ввода и текущий ввод внутри прямоугольника
        self.input_box.penup()
        # Позиционируем текст по центру прямоугольника
        self.input_box.goto(5, -10)  # Немного выше центра прямоугольника для лучшего визуального восприятия
        
        # Формируем текст для отображения
        display_text = self.current_input + "▎" if self.game_started == False else self.current_input
        # Отображаем текст по центру прямоугольника
        self.input_box.write(display_text, align="center", font=('Arial', 20, 'normal'))
        
        # Проверяем корректность ввода и показываем сообщение об ошибке, если нужно
        if self.current_input:
            if not (self.current_input.isdigit() and 
                1 <= int(self.current_input) <= 20):
                # Если ввод некорректный, показываем сообщение об ошибке
                self.input_box.goto(0, -50)  # Ниже прямоугольника
                self.input_box.color('red')
                self.input_box.write("Введите число от 1 до 20",
                                align="center", font=('Arial', 14, 'normal'))

    # Метод обработки ввода цифр
    def handle_number(self, number):
        if not self.game_started:       # Если игра еще не началась
            self.current_input += number # Добавляем цифру к текущему вводу
            self.draw_input_box()       # Перер

    # Метод обработки нажатия клавиши Backspace
    def handle_backspace(self):
        if not self.game_started:              # Если игра еще не началась
            self.current_input = self.current_input[:-1]  # Удаляем последний символ
            self.draw_input_box()              # Перерисовываем поле ввода

    # Метод обработки нажатия клавиши Enter
    def handle_enter(self):
        if not self.game_started and self.current_input:  # Если игра не началась и есть ввод
            if self.current_input.isdigit():   # Проверяем, что введено число
                score = int(self.current_input)  # Преобразуем ввод в число
                if 1 <= score <= 20:           # Проверяем диапазон
                    self.score_to_win = score  # Устанавливаем количество очков для победы
                    self.start_game()          # Начинаем игру

    # Метод запуска игры
    def start_game(self):
        self.game_started = True               # Устанавливаем флаг начала игры
        self.start_time = time.time()          # Запоминаем время начала
        
        # Очищаем экран от элементов ввода
        self.text_display.clear()              # Очищаем текст
        self.input_box.clear()                 # Очищаем поле ввода
        
        # Показываем игровые объекты
        self.show_game_objects()
        
        # Настраиваем управление
        self.screen.onkey(self.player.move_up, 'Up')     # Привязываем клавишу вверх
        self.screen.onkey(self.player.move_down, 'Down') # Привязываем клавишу вниз
        
        # Запускаем игровой цикл
        self.update()

    # Метод завершения игры
    def end_game(self, message):
        self.game_over = True                  # Устанавливаем флаг окончания игры
        self.hide_game_objects()               # Скрываем все объекты
        self.screen.update()                   # Обновляем экран

        # Вычисляем время игры
        game_time = round((time.time() - self.start_time), 2)  # Округляем до 2 знаков

        # Устанавливаем позицию для вывода сообщения
        self.text_display.goto(0, 50)     # Позиция для основного сообщения
        self.text_display.color('black')       # Устанавливаем черный цвет текста

        # Формируем и выводим сообщение о времени
        full_message = 'Время игры: ' + str(game_time) + ' сек'
        # Выводим сообщение Game over
        self.text_display.write('Game over!', align='center', font=('Arial', 30, 'bold'))
        # Перемещаем курсор для вывода времени
        self.text_display.goto(0, 0)
        # Выводим сообщение о результате
        self.text_display.write(message, align='center', font=('Arial', 30, 'bold'))
        # Перемещаем курсор для вывода времени
        self.text_display.goto(0, -50)
        # Выводим время игры
        self.text_display.write(full_message, align='center', font=('Arial', 30, 'bold'))

        # Обновляем экран
        self.screen.update()

    # Метод обновления игрового состояния
    def update(self):
        if self.game_over:                     # Если игра окончена
            return                             # Прекращаем обновление
        
        # Двигаем всех врагов
        for enemy in self.enemies:
            enemy.make_step()                  # Вызываем метод движения для каждого врага

        # Двигаем цель
        self.goal.make_step()                  # Вызываем метод движения цели
        
        # Проверяем столкновение с целью
        if self.player.is_collide(self.goal):  # Если игрок коснулся цели
            self.player.points += 1            # Увеличиваем счет
            self.player.goto(0, -150)          # Возвращаем игрока на старт

        # Проверяем столкновение с врагами
        for enemy in self.enemies:             # Для каждого врага
            if self.player.is_collide(enemy):  # Если игрок коснулся врага
                self.end_game('You lose')      # Завершаем игру поражением
                return                         # Прекращаем обновление
        
        # Проверяем условие победы
        if self.player.points >= self.score_to_win:  # Если набрано достаточно очков
            self.end_game('You win')          # Завершаем игру победой
            return                            # Прекращаем обновление

        # Обновляем экран
        self.screen.update()
        # Планируем следующее обновление через 10 миллисекунд
        self.screen.ontimer(self.update, 10)

# Создание и запуск игры
def main():
    # Создаем экземпляр игры
    game = Game()
    # Показываем начальный экран с полем ввода
    game.draw_input_box()
    # Запускаем главный цикл игры
    game.screen.mainloop()

# Запускаем игру только если этот файл запущен напрямую
if __name__ == "__main__":
    main()