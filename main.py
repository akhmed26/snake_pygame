import pygame as pg
from random import randrange
from text import *

pg.init()

RES = 800
SIZE = 50
FPS = 10

# todo: Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# todo: Функции

def get_random():
    return randrange(0, RES, SIZE), randrange(0, RES, SIZE)

def update_score_Text():
    global score, record, score_Text, record_Text
    score_Text = Text(f"Score: {score}", "arial", 25, RED)
    if score > record:
        record = score
        with open("record.txt", "w") as f:
            f.write(str(record))
        record_Text = Text(f"Record: {record}", "arial", 20, RED)
        record_Text.rect_txt.x = RES - record_Text.rect_txt.width

def update_window(bool=False):
    #  todo: Вывод Текста и Окна
    clock.tick(FPS)
    window.fill('black')
    window.blit(score_Text.text, score_Text.rect_txt)
    window.blit(record_Text.text, record_Text.rect_txt)
    if bool:
        window.blit(game_Text.text, game_Text.rect_txt)
    

    # todo: Вывод Змейки и Яблока
    [pg.draw.rect(window, GREEN, (x, y, SIZE-2, SIZE-2)) for x, y in snake]
    pg.draw.rect(window, RED, (min_apple[0] , min_apple[1],  SIZE-20, SIZE-20))
    
    if big_score >= 5 and is_big_apple:
        pg.draw.rect(window, pg.Color("yellow"), (big_apple[0], big_apple[1], SIZE, SIZE))

# todo: Змейка
SIZE = 50
x, y = get_random()
snake = [(x, y)]
dx, dy = 0, 0
length = 1

# todo: Яблоко
min_apple = get_random()
big_apple = get_random()

# todo: Счет
with open("record.txt", "r") as f:
    record = int(f.readline().strip())
score = 0
big_score = 0

BIG_APPLE = pg.USEREVENT + 1
pg.time.set_timer(BIG_APPLE, 0)

#  todo: Текст
score_Text = Text(f"Score: {score}", "arial", 25, RED)
record_Text = Text(f"Record: {record}", "arial", 20, RED)
game_Text = Text(f"Game Over", "arial", 50, RED)

record_Text.rect_txt.x = RES - record_Text.rect_txt.width
game_Text.rect_txt.center = (RES // 2, RES // 2)

#  todo: Окно
window = pg.display.set_mode((RES, RES))
pg.display.set_caption("Змейка")
pg.display.set_icon(pg.image.load("snake.png"))
clock = pg.time.Clock()


is_big_apple = False
is_time = 0


# todo: Игра
runnig = True
game = True
while runnig:
    #  todo: Если проиграл
    if not game:
        run = True
        while run:
            update_window(True)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        update_score_Text()
                        run = False
                        game = True
                        snake = [(x, y)]
                        dx, dy = 0, 0
                        length = 1
                        min_apple = get_random()
                        big_apple = get_random()
                        score = 0
                        big_score = 0
                        is_big_apple = False
                        is_time = 0
                        pg.time.set_timer(BIG_APPLE, 0)
                    
            pg.display.flip()
            
    # todo: Get_Вычисление напрвления and QUIT
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dy != 1:
                dx, dy = 0, -1
            elif event.key == pg.K_DOWN and dy != -1:
                dx, dy = 0, 1
            elif event.key == pg.K_LEFT and dx != 1:
                dx, dy = -1, 0
            elif event.key == pg.K_RIGHT and dx != -1:
                dx, dy = 1, 0
        elif event.type == BIG_APPLE:
            is_big_apple = None
            big_score = 0
            pg.time.set_timer(BIG_APPLE, 0)

    # todo : Если вышел за стенку
    if x + (SIZE * dx ) >= RES:
        x = -50
    elif x + (SIZE * dx ) < 0:
        x = RES
    elif y + (SIZE * dy) >= RES:
        y = -50
    elif y + (SIZE * dy) < 0:
        y = RES
        
    # todo: Get_Передвижение Змейки
    x += SIZE * dx 
    y += SIZE * dy
    snake.append((x, y))
    snake = snake[-length:]
 
    # todo: Сьедение яблок
    if snake[-1] == min_apple:
        big_score += 1
        score += 1
        update_score_Text()
        length += 1
        min_apple = get_random()
        
    if big_score >= 5 and not is_big_apple:
        pg.time.set_timer(BIG_APPLE, 4000)
        is_big_apple = True
        
        
    if snake[-1] == big_apple and big_score >= 5:
        pg.time.set_timer(BIG_APPLE, 0)
        score += 5
        update_score_Text()
        big_score = 0
        big_apple = get_random()
        is_big_apple = False
        
    #  todo: Момент проигрыша
    if len(snake) != len(set(snake)):
        game = False
        continue

    update_window()

    pg.display.flip()