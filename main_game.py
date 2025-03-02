# Импортируем все классы и функции из модуля turtle для создания графики
from turtle import *
# Импортируем модуль time для работы со временем
import time

# Определяем константы размеров игрового поля
s_width = 200    # Ширина поля в пикселях
s_height = 200   # Высота поля в пикселях

# Глобальные переменные для состояния игры
score_to_win = 0
game_started = False
game_over = False
start_time = 0
current_input = ""

# Глобальные переменные для объектов игры
screen = None
text_display = None
input_box = None
player = None
enemy1 = None
enemy2 = None
enemy3 = None
enemy4 = None
goal = None
enemies = []

# Базовый класс для всех объектов игры остается без изменений
class Sprite(Turtle):
    def __init__(self, x, y, step=10, shape='circle', color='orange', speed_mult=50):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.color(color)
        self.shape(shape)
        self.step = step
        self.speed(0)
        self.speed_multiplier = speed_mult
        self.direction = 1
        self.points = 0

    def move_up(self):
        self.sety(self.ycor() + self.step)

    def move_down(self):
        self.sety(self.ycor() - self.step)

    def move_left(self):
        self.setx(self.xcor() - self.step)

    def move_right(self):
        self.setx(self.xcor() + self.step)

    def is_collide(self, sprite):
        return self.distance(sprite.xcor(), sprite.ycor()) < 20

# Классы Enemy и Goal остаются без изменений
class Enemy(Sprite):
    def __init__(self, x, y, step=10, shape='circle', color='orange', speed_mult=50, start_direction=1):
        super().__init__(x, y, step, shape, color, speed_mult)
        self.direction = start_direction

    def set_move(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        
        if self.direction == -1:
            start_x = x_end
        else:
            start_x = x_start
        self.goto(start_x, y_start)

    def make_step(self):
        new_x = self.xcor() + (self.step * self.speed_multiplier * self.direction)
        self.setx(new_x)
        
        if new_x >= self.x_end or new_x <= self.x_start:
            self.direction *= -1

class Goal(Sprite):
    def make_step(self):
        self.forward(self.step * self.speed_multiplier)
        
        if self.distance(self.x_end, self.y_end) < self.step * self.speed_multiplier:
            temp_x = self.x_end
            temp_y = self.y_end
            self.x_end = self.x_start
            self.y_end = self.y_start
            self.x_start = temp_x
            self.y_start = temp_y
            self.setheading(self.towards(self.x_end, self.y_end))

    def set_move(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.goto(x_start, y_start)
        self.setheading(self.towards(x_end, y_end))

def create_game_objects():
    global player, enemy1, enemy2, enemy3, enemy4, goal, enemies
    
    # Создаем игрока
    player = Sprite(0, -150, step=10, shape='turtle', color='purple')
    player.left(90)

    # Создаем первого врага
    enemy1 = Enemy(-s_width, 0, step=0.1, shape='square', color='red', speed_mult=40, start_direction=1)
    enemy1.set_move(-s_width, 0, s_width, 0)

    # Создаем второго врага
    enemy2 = Enemy(-s_width, 70, step=0.1, shape='square', color='red', speed_mult=60, start_direction=-1)
    enemy2.set_move(-s_width, 70, s_width, 70)

    # Создаем третьего врага
    enemy3 = Enemy(-s_width, -70, step=0.1, shape='square', color='red', speed_mult=30, start_direction=1)
    enemy3.set_move(-s_width, -70, s_width, -70)

    # Создаем четвертого врага
    enemy4 = Enemy(-s_width, 140, step=0.1, shape='square', color='red', speed_mult=50, start_direction=-1)
    enemy4.set_move(-s_width, 140, s_width, 140)

    # Создаем цель
    goal = Goal(-s_width, 200, step=0.1, shape='triangle', color='green', speed_mult=50)
    goal.set_move(-s_width, s_height, s_width, s_height)

    # Создаем список всех врагов
    enemies = [enemy1, enemy2, enemy3, enemy4]

def hide_game_objects():
    player.hideturtle()
    for enemy in enemies:
        enemy.hideturtle()
    goal.hideturtle()

def show_game_objects():
    player.showturtle()
    for enemy in enemies:
        enemy.showturtle()
    goal.showturtle()

def draw_input_box():
    global current_input
    
    text_display.clear()
    input_box.clear()
    
    text_display.goto(0, 100)
    text_display.write("Введите количество очков для победы (1-20):",
                    align="center", font=('Arial', 20, 'normal'))
    
    input_box.penup()
    input_box.color('black')
    
    box_width = 70
    box_height = 50
    
    start_x = -box_width // 2
    start_y = 30
    
    input_box.goto(start_x, start_y)
    input_box.pendown()
    
    for _ in range(2):
        input_box.forward(box_width)
        input_box.right(90)
        input_box.forward(box_height)
        input_box.right(90)

    input_box.penup()
    input_box.goto(5, -10)
    
    display_text = current_input + "▎" if not game_started else current_input
    input_box.write(display_text, align="center", font=('Arial', 20, 'normal'))
    
    if current_input:
        if not (current_input.isdigit() and 1 <= int(current_input) <= 20):
            input_box.goto(0, -50)
            input_box.color('red')
            input_box.write("Введите число от 1 до 20",
                        align="center", font=('Arial', 14, 'normal'))

def handle_number(number):
    global current_input
    if not game_started:
        current_input += number
        draw_input_box()

def handle_backspace():
    global current_input
    if not game_started:
        current_input = current_input[:-1]
        draw_input_box()

def handle_enter():
    global score_to_win, game_started
    if not game_started and current_input:
        if current_input.isdigit():
            score = int(current_input)
            if 1 <= score <= 20:
                score_to_win = score
                start_game()

def end_game(message):
    global game_over
    game_over = True
    hide_game_objects()
    screen.update()

    game_time = round((time.time() - start_time), 2)

    text_display.goto(0, 50)
    text_display.color('black')

    full_message = 'Время игры: ' + str(game_time) + ' сек'
    text_display.write('Game over!', align='center', font=('Arial', 30, 'bold'))
    text_display.goto(0, 0)
    text_display.write(message, align='center', font=('Arial', 30, 'bold'))
    text_display.goto(0, -50)
    text_display.write(full_message, align='center', font=('Arial', 30, 'bold'))

    screen.update()

def update():
    if game_over:
        return
    
    for enemy in enemies:
        enemy.make_step()

    goal.make_step()
    
    if player.is_collide(goal):
        player.points += 1
        player.goto(0, -150)

    for enemy in enemies:
        if player.is_collide(enemy):
            end_game('You lose')
            return
    
    if player.points >= score_to_win:
        end_game('You win')
        return

    screen.update()
    screen.ontimer(update, 10)

def start_game():
    global game_started, start_time
    
    game_started = True
    start_time = time.time()
    
    text_display.clear()
    input_box.clear()
    
    show_game_objects()
    
    screen.onkey(player.move_up, 'Up')
    screen.onkey(player.move_down, 'Down')
    
    update()

def initialize_game():
    global screen, text_display, input_box
    
    # Создание и настройка игрового окна
    screen = Screen()
    screen.setup(800, 600)
    screen.tracer(0)
    
    # Создание объекта для отображения текста
    text_display = Turtle()
    text_display.hideturtle()
    text_display.penup()
    
    # Создание объекта для отображения поля ввода
    input_box = Turtle()
    input_box.hideturtle()
    input_box.penup()
    
    # Создаем все игровые объекты
    create_game_objects()
    # Скрываем их до начала игры
    hide_game_objects()
    
    # Настройка обработчиков событий клавиатуры
    screen.listen()
    for i in range(10):
        screen.onkey(lambda i=i: handle_number(str(i)), str(i))
    screen.onkey(handle_backspace, "BackSpace")
    screen.onkey(handle_enter, "Return")
    
    # Показываем начальный экран с полем ввода
    draw_input_box()
    
    # Запускаем главный цикл игры
    screen.mainloop()

# Запускаем игру только если этот файл запущен напрямую
if __name__ == "__main__":
    initialize_game()