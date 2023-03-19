import pygame
import sys
import random
import time

pygame.init()

# 游戏窗口大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 初始化游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇')

clock = pygame.time.Clock()

snake_size = 20
snake_speed = 15

snake_position = [100, 50]
snake_body = [[100, 50],
              [90, 50],
              [80, 50]]

food_position = [random.randrange(1, WINDOW_WIDTH//20) * snake_size,
                 random.randrange(1, WINDOW_HEIGHT//20) * snake_size]
food_spawn = True

direction = "RIGHT"
change_to = direction

score = 0

# 控制方向
def snake_direction(event, direction):
    if event.key == pygame.K_UP and direction != "DOWN":
        return "UP"
    if event.key == pygame.K_DOWN and direction != "UP":
        return "DOWN"
    if event.key == pygame.K_LEFT and direction != "RIGHT":
        return "LEFT"
    if event.key == pygame.K_RIGHT and direction != "LEFT":
        return "RIGHT"
    return direction

def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('你输了', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            change_to = snake_direction(event, direction)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if change_to == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= snake_size
    if direction == 'DOWN':
        snake_position[1] += snake_size
    if direction == 'LEFT':
        snake_position[0] -= snake_size
    if direction == 'RIGHT':
        snake_position[0] += snake_size

    snake_body.insert(0, list(snake_position))
    # if snake_position == food_position:
    #     score += 10
    #     food_spawn = False
    # else:
    #     snake_body.pop()

    # 如果蛇碰到食物，重新生成食物
    if snake_position == food_position:
        score += 10
        food_spawn = False
        snake_body.append(snake_body[-1])
    else:
        food_spawn = True

    # 更新蛇的位置
    snake_body.insert(0, list(snake_position))
    snake_body.pop()

    if not food_spawn:
        food_position = [round(random.randrange(0, WINDOW_WIDTH - snake_size) / snake_size) * snake_size,
                         round(random.randrange(0, WINDOW_HEIGHT - snake_size) / snake_size) * snake_size]
        while food_position in snake_body:
            food_position = [round(random.randrange(0, WINDOW_WIDTH - snake_size) / snake_size) * snake_size,
                             round(random.randrange(0, WINDOW_HEIGHT - snake_size) / snake_size) * snake_size]
        food_spawn = True

    screen.fill(BLACK)

    for position in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(
            position[0], position[1], snake_size, snake_size))
    pygame.draw.rect(screen, WHITE, pygame.Rect(
        food_position[0], food_position[1], snake_size, snake_size))

    if snake_position[0] < 0 or snake_position[0] >= WINDOW_WIDTH or snake_position[1] < 0 or snake_position[
        1] >= WINDOW_HEIGHT:
        game_over()

    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    pygame.display.flip()
    clock.tick(snake_speed)