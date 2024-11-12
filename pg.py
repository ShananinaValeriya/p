import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
COR = 0.8  # Коэффициент восстановления (0.0 < COR < 1.0)
MIN_SPEED = 0.1  # Минимальная скорость для остановки

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Закон сохранения импульса")




# Класс для представления шара


class Ball:
    def __init__(self, x, y, radius, color, vx, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx
        self.mass = mass

    def move(self):
        self.x += self.vx

        # Проверка границ экрана
        if self.x - self.radius < 0:  # Левый край
            self.x = self.radius
            self.vx = abs(self.vx) * COR  # Замедление
        elif self.x + self.radius > WIDTH:  # Правый край
            self.x = WIDTH - self.radius
            self.vx = -abs(self.vx) * COR  # Замедление

        # Проверка минимальной скорости для остановки
        if abs(self.vx) < MIN_SPEED:
            self.vx = 0

    def draw(self):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.radius)


def check_collision(ball1, ball2):
    distance = ((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2) ** 0.5
    return distance < (ball1.radius + ball2.radius)


def resolve_collision(ball1, ball2):
    # Обновляем скорости шаров на основе законов сохранения импульса
    v1 = ball1.vx
    v2 = ball2.vx
    m1 = ball1.mass
    m2 = ball2.mass

    ball1.vx = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2) * COR
    ball2.vx = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2) * COR

# Функция для ввода значений


def get_input():
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно Tkinter

    # Ввод масс и начальных скоростей
    mass1 = simpledialog.askfloat("Input", "Mass of Ball 1:", minvalue=0.1)
    mass2 = simpledialog.askfloat("Input", "Mass of Ball 2:", minvalue=0.1)
    vx1 = simpledialog.askfloat(
        "Input", "Initial velocity of Ball 1:", minvalue=-10, maxvalue=10)
    vx2 = simpledialog.askfloat(
        "Input", "Initial velocity of Ball 2:", minvalue=-10, maxvalue=10)

    return mass1, mass2, vx1, vx2


# Создание шаров
mass1, mass2, vx1, vx2 = get_input()
ball1 = Ball(200, HEIGHT // 2, 20, RED, vx1, mass1)
ball2 = Ball(600, HEIGHT // 2, 20, BLUE, vx2, mass2)

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
