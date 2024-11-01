import pygame
import sys

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Закон сохранения импульса")

# Класс для представления шара


class Ball:
    def __init__(self, x, y, radius, color, vx):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx

    def move(self):
        self.x += self.vx

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.radius)


def check_collision(ball1, ball2):
    distance = ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) ** 0.5
    return distance < (ball1.radius + ball2.radius)


def resolve_collision(ball1, ball2):
    # Простое разрешение столкновения с точки зрения 1D
    ball1.vx, ball2.vx = ball2.vx, ball1.vx


# Создание шаров
ball1 = Ball(200, HEIGHT // 2, 20, RED, 2)
ball2 = Ball(600, HEIGHT // 2, 20, BLUE, -2)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обновление
    ball1.move()
    ball2.move()

    if check_collision(ball1, ball2):
        resolve_collision(ball1, ball2)

    # Отрисовка
    screen.fill(WHITE)
    ball1.draw()
    ball2.draw()
    pygame.display.flip()
    pygame.time.delay(20)
