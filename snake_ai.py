# -*- coding:utf-8 -*-

"""
A snake game with AI. The snake can find and eat food automatically.
What you can do is just watching.
Since AI is only based on BFS now, it's a very dumb snake.

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
score = 0
color = (0, 255, 0)

snake_x = [5]
snake_y = [5]

snake_direction = "UP"
speed = 5

food = (1, 1)
running = True


distance = []
for y in range(row_num):
    distance.append([])
    for x in range(col_num):
        distance[y].append(8888)


def blit_grid():
    """
    画出窗口中的格子
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
    global snake_x, snake_y

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

    else:
        add_snake(new_x, new_y)


def snake_dead():
    """
    Do something while the snake is dead
    """
    print "dead"

def cal_distance():
    queue = [food]
    visited = []
    for y in range(row_num):
        for x in range(col_num):
            distance[y][x] = 9999

    distance[food[1]][food[0]] = 0

    while len(queue) != 0:
        head = queue[0]
        visited.append(head)
        up_grid = head[0], head[1] - 1
        down_grid = head[0], head[1] + 1
        left_grid = head[0] - 1, head[1]
        right_grid = head[0] + 1, head[1]

        for grid in [up_grid, down_grid, left_grid, right_grid]:
            if into_queue(grid, queue, visited):
                queue.append(grid)
                if distance[grid[1]][grid[0]] != 99999:
                    distance[grid[1]][grid[0]] = distance[head[1]][head[0]] + 1
        queue.pop(0)


def random_food():
    global food
    rand_x = random.randint(0, col_num - 1)
    rand_y = random.randint(0, row_num - 1)
    while is_snake(rand_x, rand_y) or (rand_x, rand_y) == (snake_x[0], snake_y[0]):
        rand_x = random.randint(0, col_num - 1)
        rand_y = random.randint(0, row_num - 1)

    draw_food((rand_x, rand_y))

    print "-"*80
    print "food:", food
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
    screen.blit(game_info, (width / 2 - 20, top_gap / 2 - 10))


def into_queue((x, y), queue, visited):
    if (x, y) == food:
        return False
    elif x < 0 or x >= col_num:
        return False
    elif y < 0 or y >= row_num:
        return False
    elif (x, y) in queue:
        return False
    elif (x, y) in visited:
        return False
    elif is_snake(x, y):
        return False
    else:
        return True


def can_move((x, y)):
    if x < 0 or x >= col_num:
        return False
    elif y < 0 or y >= row_num:
        return False
    elif is_snake(x, y):
        return False
    elif (x, y) == (snake_x[0], snake_y[0]):
        return False
    else:
        return True


def write_distance():
    global distance
    my_font = pygame.font.SysFont("arial", 11)
    for y in range(row_num):
        for x in range(col_num):
            dis = str(distance[y][x])
            dis_info = my_font.render(dis, True, (0, 0, 255), (255, 255, 255))
            rect = (left_gap + x * grid_size + 1, top_gap + y * grid_size+1 , grid_size-1, grid_size-1)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            screen.blit(dis_info, (left_gap + x * grid_size+1, top_gap + y * grid_size+1))
    pygame.display.update()


screen.fill((255, 255, 255))
blit_grid()
display_info()
draw_food(food)
cal_distance()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_p:
                running = not running

    if not running:
        continue

    four_dis = [99999, 99999, 99999, 99999]
    if can_move((snake_x[0], snake_y[0] - 1)):
        four_dis[0] = distance[snake_y[0] - 1][snake_x[0]]

    if can_move((snake_x[0] + 1, snake_y[0])):
        four_dis[1] = distance[snake_y[0]][snake_x[0] + 1]

    if can_move((snake_x[0], snake_y[0] + 1)):
        four_dis[2] = distance[snake_y[0] + 1][snake_x[0]]

    if can_move((snake_x[0] - 1, snake_y[0])):
        four_dis[3] = distance[snake_y[0]][snake_x[0] - 1]

    min_num = min(four_dis)

    if four_dis[0] < 99999 and distance[snake_y[0] - 1][snake_x[0]] == min_num and snake_direction != "DOWN":
            snake_direction = "UP"

    elif four_dis[1] < 99999 and distance[snake_y[0]][snake_x[0] + 1] == min_num and snake_direction != "LEFT":
            snake_direction = "RIGHT"

    elif four_dis[2] < 99999 and distance[snake_y[0] + 1][snake_x[0]] == min_num and snake_direction != "UP":
            snake_direction = "DOWN"

    elif four_dis[3] < 99999 and distance[snake_y[0]][snake_x[0] - 1] == min_num and snake_direction != "RIGHT":
            snake_direction = "LEFT"

    else:
        running = False

    if not running:
        continue

    rect = pygame.Rect(left_gap + snake_x[-1] * grid_size + 1, top_gap + snake_y[-1] * grid_size + 1,
                       grid_size - 1, grid_size - 1)
    pygame.draw.rect(screen, (255, 255, 255), rect)

    # clock.tick(speed)
    snake_move()
    cal_distance()
    draw_snake()
    pygame.display.update()
