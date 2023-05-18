import pygame
import random
import sys

# 初始化 Pygame 库
pygame.init()

# 游戏窗口的大小
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 创建游戏窗口
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 设置游戏窗口标题
pygame.display.set_caption('贪吃蛇游戏')

# 定义蛇的初始位置和大小
snake_x = 50
snake_y = 50
snake_size = 10

# 定义蛇的移动速度
snake_speed = 5

# 定义蛇的移动方向
snake_direction = 'right'

# 定义食物的初始位置和大小
food_x = random.randint(0, WINDOW_WIDTH - snake_size)
food_y = random.randint(0, WINDOW_HEIGHT - snake_size)
food_size = 10

# 定义得分
score = 0

# 定义游戏状态
game_over = False

# 定义蛇的初始长度和位置
snake_length = 1
snake_list = [(snake_x, snake_y)]

# 定义加速状态和加速开始时间
speed_up = False
speed_up_start_time = 0

# 创建 Pygame 时钟对象
clock = pygame.time.Clock()

# 绘制蛇的初始位置
pygame.draw.rect(game_window, BLACK, [snake_x, snake_y, snake_size, snake_size])

# 游戏循环
while not game_over:
    # 处理游戏事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # 获取键盘输入
    keys = pygame.key.get_pressed()

    # 根据键盘输入改变蛇的移动方向
    if keys[pygame.K_LEFT]:
        snake_direction = 'left'
    elif keys[pygame.K_RIGHT]:
        snake_direction = 'right'
    elif keys[pygame.K_UP]:
        snake_direction = 'up'
    elif keys[pygame.K_DOWN]:
        snake_direction = 'down'

    # 根据蛇的移动方向更新蛇的位置
    if snake_direction == 'left':
        snake_x -= snake_speed
    elif snake_direction == 'right':
        snake_x += snake_speed
    elif snake_direction == 'up':
        snake_y -= snake_speed
    elif snake_direction == 'down':
        snake_y += snake_speed

    # 判断蛇是否超出了游戏窗口的边界
    if snake_x < 0 or snake_x > WINDOW_WIDTH - snake_size or snake_y < 0 or snake_y > WINDOW_HEIGHT - snake_size:
        game_over = True

    # 判断蛇是否吃到了食物
    if snake_x < food_x + food_size and snake_x + snake_size > food_x and snake_y < food_y + food_size and snake_y + snake_size > food_y:
        food_x = random.randint(0, WINDOW_WIDTH - snake_size)
        food_y = random.randint(0, WINDOW_HEIGHT - snake_size)
        score += 1
        snake_length += 1

    # 在蛇的头部添加一个新的矩形
    snake_head = (snake_x, snake_y)
    snake_list.append(snake_head)

    # 如果蛇的长度超过了指定长度，则删除蛇的尾部矩形
    if len(snake_list) > snake_length:
        del snake_list[0]

    # 判断是否需要加速
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        if not speed_up:
            speed_up = True
            speed_up_start_time = pygame.time.get_ticks()
        else:
            current_time = pygame.time.get_ticks()
            if current_time - speed_up_start_time > 500:
                snake_speed *= 2
    else:
        speed_up = False
        snake_speed = 5

    # 绘制游戏窗口
    game_window.fill(WHITE)
    pygame.draw.rect(game_window, GREEN, [food_x, food_y, food_size, food_size])
    for x, y in snake_list:
        pygame.draw.rect(game_window, BLACK, [x, y, snake_size, snake_size])

    # 显示得分
    font = pygame.font.SysFont(None, 25)
    text = font.render('Score: ' + str(score), True, BLACK)
    game_window.blit(text, (10, 10))

    # 更新游戏窗口
    pygame.display.update()

    # 控制游戏循环的速度
    clock.tick(10)

# 显示游戏结束信息
font = pygame.font.SysFont(None, 50)
text = font.render('Game Over', True, RED)
game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
pygame.display.update()

# 等待一段时间后退出 Pygame 库
pygame.time.wait(2000)
pygame.quit()