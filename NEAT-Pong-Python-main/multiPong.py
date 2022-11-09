import pygame
import math
import random
pygame.init()
pygame.font.init()


WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # sets window
pygame.display.set_caption("Pong")  # Title for Window


SCORE_FONT = pygame.font.SysFont('comicsans', 50)
WINNER_FONT = pygame.font.SysFont('comicsans', 35)

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100


class Paddle:
    COLOR = WHITE
    VEL = 7

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)

    pygame.display.update()


class Ball:
    MAX_VEL = 9
    RADIUS = 7

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1

        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.RADIUS)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.MAX_VEL)
        y_vel = math.sin(angle) * self.MAX_VEL

        self.y_vel = y_vel
        self.x_vel *= -1


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VEL <= HEIGHT:
        right_paddle.move(up=False)


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.RADIUS >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.RADIUS <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if (ball.y >= left_paddle.y) and (ball.y <= left_paddle.y + left_paddle.height):
            if ball.x - ball.RADIUS <= left_paddle.x + left_paddle.width:


                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / 5
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if (ball.y >= right_paddle.y) and (ball.y <= right_paddle.y + right_paddle.height):
            if ball.x + ball.RADIUS >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / 5
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def draw_winner(text, win):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    if text == "Left Player Won":
        WIN.blit(draw_text, (WIDTH / 4 - draw_text.get_width() / 2, HEIGHT / 4 - draw_text.get_height()/2))
    elif text == "Right Player Won":
        WIN.blit(draw_text, (WIDTH * (3/4) - draw_text.get_width() / 2, HEIGHT / 4 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def play_multi():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        if left_score >= 5:
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
            pygame.time.delay(200)
            text = "Left Player Won"
            draw_winner(text, WIN)
            break
        if right_score >= 5:
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
            pygame.time.delay(200)
            text = "Right Player Won"
            draw_winner(text, WIN)
            break

    play_multi()


if __name__ == '__main__':
    play_multi()
