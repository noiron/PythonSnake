# -*- coding:utf-8 -*-

"""
A snake game without AI. This code has no class.

Press "up", "down", "left", "right" or "w,a,s,d"to play, press "p" to pause.

Author:Wukai
Time:2015/05/18

"""

import pygame
from pygame.locals import *
import random

pygame.init()

width = 600
height = 400
grid_size = 20
col_num = width / grid_size
row_num = height / grid_size
top_gap = 70
left_gap = 30

screen = pygame.display.set_mode((width + left_gap * 2, height + top_gap * 2), 0, 32)
clock = pygame.time.Clock()
# font = pygame.font.SysFont('Comic Sans MS', 40)
score = 0
color = (0, 255, 0)

snake_x = range(8, 6, -1)
snake_y = [8] * 2
snake_direction = "RIGHT"
speed = 4

food = (4, 4)
running = True


def blit_grid():
    """
    Draw the grids in the game window.
    """
    for x in range(1, col_num):
        pygame.draw.aaline(screen, (0, 0, 0),
                           (left_gap + x * grid_size, top_gap),
                           (left_gap + x * grid_size, height + top_gap))
    for y in range(1, row_num):
        pygame.draw.aaline(screen, (0, 0, 0),
                           (left_gap, y * grid_size + top_gap),
                           (width + 30, y * grid_size + top_gap))

    # draw the top border
    pygame.draw.line(screen, (0, 0, 0), (left_gap - 2, top_gap - 2), (width + left_gap, top_gap - 2), 3)
    # draw the bottom border
    pygame.draw.line(screen, (0, 0, 0), (left_gap - 2, top_gap + height), (width + left_gap, top_gap + height), 3)
    # draw the left border
    pygame.draw.line(screen, (0, 0, 0), (left_gap - 2, top_gap - 2), (left_gap - 2, top_gap + height), 3)
    # draw the right border
    pygame.draw.line(screen, (0, 0, 0), (left_gap + width, top_gap - 2), (left_gap + width, top_gap + height), 3)


def draw_snake():
    """
    Draw the snake by snake_x and snake_y
    """
    for i in range(0, len(snake_x)):
        rect = pygame.Rect(left_gap + snake_x[i] * grid_size + 1,
                           top_gap + snake_y[i] * grid_size + 1,
                           grid_size - 1, grid_size - 1)
        pygame.draw.rect(screen, color, rect)

    # Draw the head with a different color
    rect = pygame.Rect(left_gap + snake_x[0] * grid_size + 1,
                       top_gap + snake_y[0] * grid_size + 1,
                       grid_size - 1, grid_size - 1)
    pygame.draw.rect(screen, (100, 100, 100), rect)
    pygame.display.update()


def is_snake(x, y):
    """
    Judge if (x,y) is part of the snake except the head.
    """
    if (x, y) in zip(snake_x[1:], snake_y[1:]):
        return True
    else:
        return False


def add_snake(new_x, new_y):
    global food
    snake_x.insert(0, new_x)
    snake_y.insert(0, new_y)
    if (new_x, new_y) != food:
        del snake_x[-1], snake_y[-1]
    else:
        food = random_food()


def snake_move():
    if snake_direction == "LEFT":
        new_x = snake_x[0] - 1
        new_y = snake_y[0]

    elif snake_direction == "RIGHT":
        new_x = snake_x[0] + 1
        new_y = snake_y[0]

    elif snake_direction == "UP":
        new_x = snake_x[0]
        new_y = snake_y[0] - 1

    elif snake_direction == "DOWN":
        new_x = snake_x[0]
        new_y = snake_y[0] + 1

    if new_x < 0 or new_x >= col_num or new_y < 0 or new_y >= row_num:
        snake_dead()
    elif is_snake(new_x, new_y):
        snake_dead()
    else:
        add_snake(new_x, new_y)


def snake_dead():
    """
    Do something while the snake is dead
    """
    print "dead"


def random_food():
    rand_x = random.randint(0, col_num - 1)
    rand_y = random.randint(0, row_num - 1)
    while is_snake(rand_x, rand_y) or (rand_x, rand_y) == (snake_x[0], snake_y[0]):
        rand_x = random.randint(0, col_num - 1)
        rand_y = random.randint(0, row_num - 1)
    draw_food((rand_x, rand_y))

    return rand_x, rand_y


def draw_food((x, y)):
    rect = pygame.Rect(left_gap + x * grid_size + 1, top_gap + y * grid_size + 1,
                       grid_size - 1, grid_size - 1)
    pygame.draw.rect(screen, (255, 0, 0), rect)
    pygame.display.update()


def display_info():
    my_font = pygame.font.SysFont('Comic Sans MS', 25)
    title = "Snake Game"
    game_info = my_font.render(title, True, (0, 0, 0), (186, 120, 158))
    screen.blit(game_info, (width/2-20, top_gap/2-10))


screen.fill((255, 255, 255))
blit_grid()
display_info()
draw_food(food)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_p:
                running = not running

            if event.key == K_LEFT or event.key == K_a and snake_direction != "RIGHT":
                snake_direction = "LEFT"

            elif event.key == K_RIGHT or event.key == K_d and snake_direction != "LEFT":
                snake_direction = "RIGHT"

            elif event.key == K_UP or event.key == K_w and snake_direction != "DOWN":
                snake_direction = "UP"

            elif event.key == K_DOWN or event.key == K_s and snake_direction != "UP":
                snake_direction = "DOWN"

    if not running:
        continue

    rect = pygame.Rect(left_gap + snake_x[-1] * grid_size + 1, top_gap + snake_y[-1] * grid_size + 1,
                       grid_size - 1, grid_size - 1)
    pygame.draw.rect(screen, (255, 255, 255), rect)

    clock.tick(speed)
    snake_move()
    draw_snake()

    pygame.display.update()
