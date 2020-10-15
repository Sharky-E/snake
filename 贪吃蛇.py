import pygame,sys, random, time
# 从pygame模块导入常用的函数和常量
from pygame.locals import *
# 一些全局参数的初始化


def main():
    global FPSCLOCK, DISPLAY, BASICFONT, BLACK, WHITE, GREEN, GREY

    # 初始化Pygame库
    pygame.init()
    # 初始化一个游戏界面窗口
    DISPLAY = pygame.display.set_mode((640, 480))
    # 设置游戏窗口的标题
    pygame.display.set_caption('Snake')
    # 定义一个变量来控制游戏速度
    FPSCLOCK = pygame.time.Clock()
    # 初始化游戏界面内使用的字体
    BASICFONT = pygame.font.SysFont("黑体", 30)

    # 定义颜色变量
    BLACK = (0, 0, 0, 55)
    WHITE = (255, 255, 255, 55)
    GREEN = (0, 255, 0, 55)
    GREY = (150, 150, 150, 55)

    play_game()


# 开始游戏
def play_game():

    # 贪吃蛇的的初始位置
    snake_head = [60, 100]
    # 初始化贪吃蛇的长度 (注：这里以20*20为一个标准小格子)
    snake_body = [[60, 100], [40, 100], [20, 100]]
    # 指定蛇初始前进的方向，向右
    direction = "right"

    # 给定第一枚食物的位置
    # 随机生成x, y
    x = random.randrange(1, 32)
    y = random.randrange(1, 24)
    food_position = [int(x * 20), int(y * 20)]
    # 食物标记：0代表食物已被吃掉；1代表未被吃掉。
    food_flag = 1

    '''游戏的主循环'''
    while True:
        # 检测按键等Pygame事件
        for event in pygame.event.get():
            if event.type == QUIT :
                # 接收到退出事件后，退出程序
                pygame.quit()
                sys.exit()

            # 判断键盘事件，用 方向键 或 w,s,a,d 来表示上下左右
            elif event.type == KEYDOWN:
                if (event.key == K_UP or event.key == K_w) and direction != 'down':
                    direction = 'up'
                if (event.key == K_DOWN or event.key == K_s) and direction != 'up':
                    direction = 'down'
                if (event.key == K_LEFT or event.key == K_a) and direction != 'right':
                    direction = 'left'
                if (event.key == K_RIGHT or event.key == K_d) and direction != 'left':
                    direction = 'right'
                if (event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        # 根据键盘的输入，改变蛇的头部，进行转弯操作
        if direction == 'left':
            snake_head[0] -= 20
        if direction == 'right':
            snake_head[0] += 20
        if direction == 'up':
            snake_head[1] -= 20
        if direction == 'down':
            snake_head[1] += 20

        # 将蛇的头部当前的位置加入到蛇身的列表中
        snake_body.insert(0, list(snake_head))

        # 判断是否吃掉食物
        if snake_head[0] == food_position[0] and snake_head[1] == food_position[1]:
            food_flag = 0
        else:
            snake_body.pop()

        # 生成新的食物
        if food_flag == 0:
            x = random.randrange(1, 32)
            y = random.randrange(1, 24)
            food_position = [int(x * 20), int(y * 20)]
            food_flag = 1

        DISPLAY.fill(BLACK)
        # 画出贪吃蛇
        draw_snake(snake_body)
        # 画出食物的位置
        draw_food(food_position)
        # 打印出玩家的分数
        draw_score(len(snake_body) - 3)
        # 刷新Pygame的显示层
        pygame.display.flip()
        # 控制游戏速度
        FPSCLOCK.tick(7)

        '''游戏结束的判断'''
        # 贪吃蛇触碰到边界
        if snake_head[0] < 0 or snake_head[0] > 620:
            game_over()
        if snake_head[1] < 0 or snake_head[1] > 460:
            game_over()
        # 贪吃蛇触碰到自己
        for i in snake_body[1:]:
            if snake_head[0] == i[0] and snake_head[1] == i[1]:
                game_over()


# 画出贪吃
def draw_snake(snake_body):
    for i in snake_body:
        pygame.draw.rect(DISPLAY, WHITE, Rect(i[0], i[1], 20, 20))


# 画出食物的位置
def draw_food(food_position):
    pygame.draw.rect(DISPLAY, GREEN, Rect(food_position[0], food_position[1], 20, 20))


# 打印出当前得分
def draw_score(score):
    # 设置分数的显示颜色大小
    score_show = BASICFONT.render("Score:", True, GREY)
    score_surf = BASICFONT.render('%s' % (score), True, GREY)
    # 设置分数的位置
    score_rect = score_surf.get_rect()
    score_rect.midtop = (600, 450)
    score_rect2 = score_show.get_rect()
    score_rect2.midtop = (550, 450)
    # 绑定以上设置到句柄
    DISPLAY.blit(score_surf, score_rect)
    DISPLAY.blit(score_show, score_rect2)


def game_over():
    # 设置GameOver的显示颜色
    game_over_font = pygame.font.SysFont("impact", 80)
    game_over_surf = game_over_font.render('Game Over!', True, GREY)
    # 设置GameOver的位置
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (320, 180)

    # 设置退出提示
    game_over_font2 = pygame.font.SysFont('SimHei', 20)
    game_over_esc = game_over_font2.render('按ESC退出游戏', True, GREY)
    game_over_rect2 = game_over_esc.get_rect()
    game_over_rect2.midtop = (70, 10)

    # 绑定以上设置到句柄
    DISPLAY.blit(game_over_surf, game_over_rect)
    DISPLAY.blit(game_over_esc, game_over_rect2)

    pygame.display.flip()
    # 等待3秒
    time.sleep(3)
    # 继续游戏
    play_game()


# 运行主函数
if __name__ == "__main__":
    main()