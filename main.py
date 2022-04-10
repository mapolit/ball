import sys
import pygame
import random
import math
import time

W, H = (800, 400)  # 屏幕
WHITE = (255, 255, 255)  # 颜色定义

pygame.init()  # 初始化
SCREEN = pygame.display.set_mode((W, H))  # 屏幕定义
pygame.display.set_caption("ball!")  # 标题设置
CLOCK = pygame.time.Clock()  # 定义 钟
FONT = pygame.font.SysFont("Consolas.ttf", 50)  # 显示字体定义, 字号50


# 定义玩家
class Player:
    def __init__(self, player):
        self.player = player
        self.score = 0  # 玩家分数
        self.width = 5  # 板板宽度
        self.height = 50  # 板板长度
        self.x = 0 if self.player == 1 else W - self.width  # 两玩家x坐标
        self.y = (H - self.height) / 2  # y坐标
        self.y_v = 5  # 移动速度
        self.lose = False  # 是否输了

    # 更新
    def update(self, keys):
        if self.player == 1:
            if keys[pygame.K_w]:
                self.y -= self.y_v
            elif keys[pygame.K_s]:
                self.y += self.y_v
        elif self.player == 2:
            if keys[pygame.K_UP]:
                self.y -= self.y_v
            elif keys[pygame.K_DOWN]:
                self.y += self.y_v

        # 防止溜出屏幕
        if self.y <= 0:
            self.y = 0
        elif self.y + self.height >= H:
            self.y = H - self.height

    # 画板板
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))


# 要玩的球
class Ball:
    def __init__(self):
        self.x = W / 2  # 初始x
        self.y = H / 2  # 初始y
        self.r = 5  # 半径
        # 速度随机
        self.x_v = random.choice([-2, 2]) * 3
        self.y_v = random.choice([1, 2, 3]) * random.choice([-1, 1])
        # 颜色(无聊的玩法)
        self.count_r = 100
        self.count_g = 100
        self.count_b = 100
        self.color = (self.count_r, self.count_g, self.count_b)

    # 更新
    def update(self):
        self.x += self.x_v
        self.y += self.y_v

        # 反弹(dang)
        if self.y <= 0 or self.y >= H:
            self.y_v *= -1

        # 颜色更新(太无聊了吧)
        if self.count_r > 255:
            self.count_r = 100
            self.count_g += 10
        if self.count_g > 255:
            self.count_g = 100
            self.count_b += 10
        if self.count_b > 255:
            self.count_b = 100

    # 画球球
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


# 人工智障
class AI(Player):
    def __init__(self, player, ball):
        Player.__init__(self, player)
        self.get_ball = ball  # 绑定球
        self.up_down = random.randrange(0, 16)  # 误差

    # 更新
    def update(self, keys):
        Player.update(self, keys)
        if self.player == 1:
            if self.get_ball.x <= W / 2:
                if self.y + self.height / 2 > self.get_ball.y + self.up_down:
                    self.y -= self.y_v
                elif self.y + self.height / 2 < self.get_ball.y - self.up_down:
                    self.y += self.y_v
        elif self.player == 2:
            if self.get_ball.x >= W / 2:
                if self.y + self.height / 2 > self.get_ball.y + self.up_down:
                    self.y -= self.y_v
                elif self.y + self.height / 2 < self.get_ball.y - self.up_down:
                    self.y += self.y_v


# 主程序
def main():
    title()
    while True:
        time.sleep(0.5)  # 防止跳太快
        player = begin()  # 参数传递
        player = game(player)
        end(player)


# 标题
def title():
    keys = pygame.key.get_pressed()
    timer = 0
    while True:
        # 按键侦测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            elif event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            return
        if keys[pygame.K_q]:
            sys.exit()

        title_main = FONT.render("B A L L", True, WHITE)  # 主标题
        current_time = pygame.time.get_ticks()
        title_small = FONT.render("press [ENTER] to start", True, WHITE)  # 副标题

        title_main = pygame.transform.scale(title_main, (title_main.get_width() * 2, title_main.get_height() * 2))
        title_small = pygame.transform.scale(title_small, (title_small.get_width() / 2, title_small.get_height() / 2))

        # 获取长宽
        title_main_width = title_main.get_width()
        title_main_height = title_main.get_height()
        title_small_width = title_small.get_width()
        # 定位
        title_main_x = (W - title_main_width) / 2
        title_main_y = H / 2 - title_main_height
        title_small_x = (W - title_small_width) / 2
        title_small_y = H / 2

        SCREEN.fill(0)
        SCREEN.blit(title_main, (title_main_x, title_main_y))
        if current_time - timer >= 3000:
            SCREEN.blit(title_small, (title_small_x, title_small_y))

        pygame.display.update()
        CLOCK.tick(60)


# 主菜单
def begin():
    countdown = 6
    change_time = 0
    player1 = Player(1)
    player2 = Player(2)
    player1_check = False
    player2_check = False
    continue_game = False
    player1_AI = False
    player2_AI = False
    keys = pygame.key.get_pressed()
    while True:
        # 按键侦测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            elif event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            player2_check = True
        if keys[pygame.K_w] or keys[pygame.K_s]:
            player1_check = True

        # 谁是AI？
        if player1_check and player2_check:
            if not continue_game:
                current = pygame.time.get_ticks()
                if current - change_time >= 1000:
                    change_time = current
                    countdown -= 1
                if countdown <= 0:
                    continue_game = True
        elif player1_check and keys[pygame.K_RETURN]:
            print('p2 is AI!')
            if not continue_game:
                continue_game = True
                player2_AI = True
        elif player2_check and keys[pygame.K_RETURN]:
            print('p1 is AI!')
            if not continue_game:
                continue_game = True
                player1_AI = True
        elif keys[pygame.K_RETURN]:
            print('both two players are AI!')
            if not continue_game:
                continue_game = True
                player2_AI = True
                player1_AI = True

        if continue_game:
            if player1_AI and player2_AI:
                return ['ai', 'ai']  # 都是AI
            elif player1_AI:
                return ['ai', player2]  # p1是
            elif player2_AI:
                return [player1, 'ai']  # p2是
            else:
                return [player1, player2]  # 都不是

        player1.update(keys)
        player2.update(keys)

        # 画
        SCREEN.fill(0)
        player1.draw(SCREEN)
        player2.draw(SCREEN)

        # test text
        if not player1_check:
            p1_check_text = FONT.render("test: 'w':up   's':down", True, WHITE)
            p1_check_text = pygame.transform.scale(p1_check_text,
                                                   (p1_check_text.get_width() / 2, p1_check_text.get_height() / 2))
            p1ct_x = (W / 2 - p1_check_text.get_width()) / 2
            p1ct_y = 20
            SCREEN.blit(p1_check_text, (p1ct_x, p1ct_y))
        if not player2_check:
            p2_check_text = FONT.render("test: 'UP':up   'DOWN':down", True, WHITE)
            p2_check_text = pygame.transform.scale(p2_check_text,
                                                   (p2_check_text.get_width() / 2, p2_check_text.get_height() / 2))
            p2ct_x = (W * 3 / 2 - p2_check_text.get_width()) / 2
            p2ct_y = 20
            SCREEN.blit(p2_check_text, (p2ct_x, p2ct_y))

        # 都就位后继续
        if player1_check and player2_check:
            count = FONT.render(str(countdown), True, WHITE)
            SCREEN.blit(count, ((W - count.get_width()) / 2, (H - count.get_height()) / 2))

        # 帮助信息
        text_help = FONT.render("this is help info:", True, WHITE)
        if countdown == 4 or countdown == 3:
            text_help = FONT.render("when two players press 'left' and 'right' at the same time, "
                                    "then the game will finish", True, WHITE)
        elif countdown == 2:
            text_help = FONT.render("press 'right' can add the score of a ball", True, WHITE)
        elif countdown <= 1:
            text_help = FONT.render("have a good time", True, WHITE)
        text_help = pygame.transform.scale(text_help, (text_help.get_width() / 2, text_help.get_height() / 2))
        if player1_check and player2_check:
            text_help_x = (W - text_help.get_width()) / 2
            text_help_y = (H - text_help.get_height()) / 2 - 20
            SCREEN.blit(text_help, (text_help_x, text_help_y))

        # 标准更新
        pygame.display.update()
        CLOCK.tick(60)


# 主体
def game(player):
    ball = Ball()
    player1 = player[0]
    player2 = player[1]
    if player1 == 'ai':
        player1 = AI(1, ball)
    if player2 == 'ai':
        player2 = AI(2, ball)
    keys = pygame.key.get_pressed()
    add_score = 1
    can_add = True
    while True:
        # 按键侦测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            elif event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()

        # 触板反弹
        if ball.x - ball.r == player1.x + player1.width and player1.y <= ball.y <= player1.y + player1.height:
            ball.count_r += 10
            ball.x_v *= -1
            ball.y_v = math.fabs(ball.x_v) * ((ball.y - (player1.y + player1.height / 2)) / (player1.height / 2))
        elif ball.x + ball.r == player2.x and player2.y <= ball.y <= player2.y + player2.height:
            ball.count_r += 10
            ball.x_v *= -1
            ball.y_v = math.fabs(ball.x_v) * ((ball.y - (player2.y + player2.height / 2)) / (player2.height / 2))

        # 输赢判断
        if ball.x >= W:
            player1.score += add_score
            del ball
            ball = Ball()
            add_score = 1
            if player[0] == 'ai':
                player1.get_ball = ball
            if player[1] == 'ai':
                player2.get_ball = ball
        if ball.x <= 0:
            player2.score += add_score
            del ball
            ball = Ball()
            add_score = 1
            if player[0] == 'ai':
                player1.get_ball = ball
            if player[1] == 'ai':
                player2.get_ball = ball

        if keys[pygame.K_a] and keys[pygame.K_d] and keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            return [player1, player2]

        if keys[pygame.K_q]:
            player1.lose = True
            return [player1, player2]
        if keys[pygame.K_RSHIFT]:
            player2.lose = True
            return [player1, player2]

        if can_add:
            if keys[pygame.K_d]:
                add_score += 1
                can_add = False
            if keys[pygame.K_RIGHT]:
                add_score += 1
                can_add = False
        else:
            if not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                can_add = True

        player1.update(keys)
        player2.update(keys)
        ball.update()

        # 画
        SCREEN.fill(0)

        score_pic = FONT.render("{}     {}".format(player1.score, player2.score), True, WHITE)
        SCREEN.blit(score_pic, ((W - score_pic.get_width()) / 2, 10))
        add_score_pic = FONT.render("every ball : {} scores".format(add_score), True, WHITE)
        add_score_pic = pygame.transform.scale(add_score_pic,
                                               (add_score_pic.get_width() / 2, add_score_pic.get_height() / 2))
        add_score_pic_y = 10 + score_pic.get_height()
        SCREEN.blit(add_score_pic, ((W - add_score_pic.get_width()) / 2, add_score_pic_y))

        ball.draw(SCREEN)
        player1.draw(SCREEN)
        player2.draw(SCREEN)

        pygame.display.update()
        CLOCK.tick(60)


# 结束
def end(player):
    keys = pygame.key.get_pressed()
    player1 = player[0]
    player2 = player[1]
    changing_time = 0
    stop_t = 6
    while True:
        # 按键侦测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            elif event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()

        current = pygame.time.get_ticks()
        if current - changing_time >= 1000:
            changing_time = current
            stop_t -= 1
        if stop_t <= 0:
            return

        # 回车提前结束
        if keys[pygame.K_RETURN]:
            return

        player1.update(keys)
        player2.update(keys)

        SCREEN.fill(0)
        # 谁赢？

        # 认输
        if player1.lose:
            win_txt = FONT.render("p2 win!", True, WHITE)
            win_x = (W * 3 / 2 - win_txt.get_width()) / 2
            win_y = (H - win_txt.get_height()) / 2
            SCREEN.blit(win_txt, (win_x, win_y))
        elif player2.lose:
            win_txt = FONT.render("p1 win!", True, WHITE)
            win_x = (W / 2 - win_txt.get_width()) / 2
            win_y = (H - win_txt.get_height()) / 2
            SCREEN.blit(win_txt, (win_x, win_y))
        # 正常结束
        else:
            if player1.score > player2.score:
                win_txt = FONT.render("p1 win!", True, WHITE)
                win_x = (W / 2 - win_txt.get_width()) / 2
                win_y = (H - win_txt.get_height()) / 2
                SCREEN.blit(win_txt, (win_x, win_y))
            elif player1.score < player2.score:
                win_txt = FONT.render("p2 win!", True, WHITE)
                win_x = (W * 3 / 2 - win_txt.get_width()) / 2
                win_y = (H - win_txt.get_height()) / 2
                SCREEN.blit(win_txt, (win_x, win_y))
            else:
                win_txt = FONT.render("nobody win!", True, WHITE)
                win_x = (W - win_txt.get_width()) / 2
                win_y = (H - win_txt.get_height()) / 2
                SCREEN.blit(win_txt, (win_x, win_y))
        player1.draw(SCREEN)
        player2.draw(SCREEN)

        pygame.display.update()
        CLOCK.tick(60)


# 尽情游玩吧
main()
