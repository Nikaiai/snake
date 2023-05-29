import pygame
from random import randint
import os

diffcl = input(f"введите сложность(нуб, нормально, сильный, про) \nили напишите очистка чтобы удалить"
               f" рекорд(потребуется снова выбрать сложность): ")

resolution = (1920, 980)

pygame.font.init()
speed = pygame.font.SysFont('candara', 25)
score = pygame.font.SysFont('candara', 25)
dead = pygame.font.SysFont('impact', 40)
diffclt = pygame.font.SysFont('candara', 25)
nuke = pygame.font.SysFont('candara', 25)
restart = pygame.font.SysFont('impact', 25)

display = pygame.display.set_mode(resolution)

if diffcl == 'очистка':
    if os.path.isfile('record'):
        os.remove('record')
    cube = 30
    fps = 5
    diffcl = input('введите сложность(нуб, нормально, сильный, про): ')

if diffcl == 'нуб':
    cube = 30
    fps = 5
elif diffcl == 'нормально':
    cube = 30
    fps = 10
elif diffcl == 'сильный':
    cube = 32
    fps = 15
elif diffcl == 'про':
    cube = 40
    fps = 25
else:
    cube = 30
    fps = 5
    diffcl = 'нуб(неправильный изначальный ввод)'

fps_start = fps

mapa = resolution[0] // cube, resolution[1] // cube

df_pos = mapa[0] // 2, mapa[1] // 2

snake = [df_pos]

live = True

napr = 0
naprs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

apple = randint(2, mapa[0]-1), randint(2, mapa[1]-1)

clock = pygame.time.Clock()

run = True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, ochki):
    rec = max(int(record), ochki)
    with open('record', 'w') as f:
        f.write(str(rec))


pygame.time.delay(3000)

while run is True:
    record = get_record()
    ochki = len(snake)
    clock.tick(fps)
    display.fill('black')

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        if i.type == pygame.KEYDOWN:
            if live is True:
                if i.key == pygame.K_RIGHT and napr != 2:
                    napr = 0
                if i.key == pygame.K_DOWN and napr != 3:
                    napr = 1
                if i.key == pygame.K_LEFT and napr != 0:
                    napr = 2
                if i.key == pygame.K_UP and napr != 1:
                    napr = 3
            else:
                if i.key == pygame.K_SPACE:
                    live = True
                    snake = [df_pos]
                    apple = randint(0, mapa[0] - 1), randint(0, mapa[1] - 1)
                    fps = fps_start
                    napr = 0

    [pygame.draw.rect(display, 'green', (x * cube, y * cube, cube - 1, cube - 1))for x, y in snake]
    pygame.draw.rect(display, 'red', (apple[0] * cube, apple[1] * cube, cube - 1, cube - 1))

    if live is True:
        new_pos = snake[0][0] + naprs[napr][0], snake[0][1] + naprs[napr][1]
        if not (0 <= new_pos[0] < mapa[0] and 0 <= new_pos[1] < mapa[1]) or new_pos in snake:
            live = False
        else:
            snake.insert(0, new_pos)
            if new_pos == apple:
                fps += fps_start//10
                apple = randint(0, mapa[0]-1), randint(0, mapa[1]-1)
            else:
                snake.pop(-1)
    else:
        end_text = dead.render(f"ИГРА ОКОНЧЕНА", True, "white")

        display.blit(end_text, (resolution[0] // 2 - end_text.get_width() // 2, resolution[1] // 2))
        restart_text = (restart.render('нажмите пробел, чтобы начать заново', True, 'white'))
        display.blit(restart_text, (resolution[0] // 2 - restart_text.get_width() // 2, resolution[1] // 2 + 60))
        set_record(record, ochki)
    dj = nuke.render(f'ваш рекорд: {record}', True, 'white')
    dj2 = diffclt.render(f'сложность: {diffcl}', True, 'white')
    dj3 = restart.render('нажмите пробел, чтобы начать заново', True, 'white')
    display.blit(speed.render(f'текущая скорость: {fps}', True, 'white'), (5, 35))
    display.blit(score.render(f"ваши очки: {len(snake)-1}", True, "white"), (5, 5))
    display.blit(dj2, (5, resolution[1] - dj2.get_height() - 5))
    display.blit(dj, (resolution[0] - dj.get_width() - 5, 5))

    pygame.display.flip()
