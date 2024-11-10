import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class ImpulseLawApp:
    def __init__(self, master):
        self.master = master
        master.title("Закон сохранения импульса")

        # Создаем вкладки
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        # Вкладка теории
        self.theory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.theory_tab, text='Теория')
        self.create_theory_tab()

        # Вкладка вычисления импульса
        self.calculation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.calculation_tab, text='Вычисление импульса')
        self.create_calculation_tab()

        # Вкладка графиков (по умолчанию отключена)
        self.graph_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text='Графики')
        self.create_graph_tab()
        # Отключаем вкладку графиков
        self.notebook.tab(self.graph_tab, state='disabled')

        # Вкладка демонстрации (по умолчанию отключена)
        self.demo_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.demo_tab, text='Демонстрация')
        self.create_demo_tab()
        # Отключаем вкладку демонстрации
        self.notebook.tab(self.demo_tab, state='disabled')

        # Вкладка примеров
        self.examples_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.examples_tab, text='Примеры')
        self.create_examples_tab()

    def create_theory_tab(self):
        theory_text = "Импульс (p) = масса (m) * скорость (v)\n" \
                      "Закон сохранения импульса гласит, что в замкнутой системе " \
                      "импульс сохраняется, если на систему не действуют внешние силы."
        theory_label = tk.Label(
            self.theory_tab, text=theory_text, justify='left', wraplength=400)
        theory_label.pack(padx=10, pady=10)

    def create_calculation_tab(self):
        self.mass1_label = tk.Label(
            self.calculation_tab, text="Масса первого тела (kg):")
        self.mass1_label.pack()
        self.mass1_entry = tk.Entry(self.calculation_tab)
        self.mass1_entry.pack()

        self.velocity1_label = tk.Label(
            self.calculation_tab, text="Скорость первого тела (m/s):")
        self.velocity1_label.pack()
        self.velocity1_entry = tk.Entry(self.calculation_tab)
        self.velocity1_entry.pack()

        self.mass2_label = tk.Label(
            self.calculation_tab, text="Масса второго тела (kg):")
        self.mass2_label.pack()
        self.mass2_entry = tk.Entry(self.calculation_tab)
        self.mass2_entry.pack()

        self.velocity2_label = tk.Label(
            self.calculation_tab, text="Скорость второго тела (m/s):")
        self.velocity2_label.pack()
        self.velocity2_entry = tk.Entry(self.calculation_tab)
        self.velocity2_entry.pack()

        self.calculate_button = tk.Button(
            self.calculation_tab, text="Рассчитать импульс", command=self.calculate_impulse)
        self.calculate_button.pack(pady=10)

        # Поле для отображения результатов
        self.result_label = tk.Label(
            self.calculation_tab, text="", wraplength=400)
        self.result_label.pack(pady=10)

    def create_graph_tab(self):
        self.graph_button = tk.Button(
            self.graph_tab, text="Построить график", command=self.visualize_graph)
        self.graph_button.pack(pady=10)

    def create_demo_tab(self):
        self.demo_button = tk.Button(
            self.demo_tab, text="Демонстрация столкновения", command=self.visualize_collision)
        self.demo_button.pack(pady=10)

    def create_examples_tab(self):
        self.example1_button = tk.Button(
            self.examples_tab, text="Пример 1", command=self.example_collision_1)
        self.example1_button.pack(pady=10)

        self.example2_button = tk.Button(
            self.examples_tab, text="Пример 2", command=self.example_collision_2)
        self.example2_button.pack(pady=10)

        self.example3_button = tk.Button(
            self.examples_tab, text="Пример 3", command=self.example_collision_3)
        self.example3_button.pack(pady=10)

    def validate_inputs(self, m1, v1, m2, v2):
        if m1 <= 0:
            messagebox.showerror(
                "Ошибка", "Масса первого тела должна быть положительной и не равной нулю.")
            return False
        if m2 <= 0:
            messagebox.showerror(
                "Ошибка", "Масса второго тела должна быть положительной и не равной нулю.")
            return False
        if v1 < 0:
            messagebox.showerror(
                "Ошибка", "Скорость первого тела не может быть отрицательной.")
            return False
        if v2 < 0:
            messagebox.showerror(
                "Ошибка", "Скорость второго тела не может быть отрицательной.")
            return False
        return True

    def calculate_impulse(self):
        try:
            m1 = float(self.mass1_entry.get())
            v1 = float(self.velocity1_entry.get())
            m2 = float(self.mass2_entry.get())
            v2 = float(self.velocity2_entry.get())

            if not self.validate_inputs(m1, v1, m2, v2):
                return

            impulse1 = m1 * v1
            impulse2 = m2 * v2
            total_impulse = impulse1 + impulse2

            result_text = (f"Импульс первого тела: {impulse1:.2f} kg*m/s\n"
                           f"Импульс второго тела: {impulse2:.2f} kg*m/s\n"
                           f"Общий импульс: {total_impulse:.2f} kg*m/s")
            # Обновляем текстовое поле с результатами
            self.result_label.config(text=result_text)

            # Активируем вкладки графиков и демонстрации
            self.notebook.tab(self.graph_tab, state='normal')
            self.notebook.tab(self.demo_tab, state='normal')

        except ValueError:
            messagebox.showerror(
                "Ошибка", "Пожалуйста, введите корректные числовые значения.")

    def visualize_graph(self):
        try:
            m1 = float(self.mass1_entry.get())
            v1 = float(self.velocity1_entry.get())
            m2 = float(self.mass2_entry.get())
            v2 = float(self.velocity2_entry.get())

            if not self.validate_inputs(m1, v1, m2, v2):
                return

        # Параметры для графика
            t = np.linspace(0, 2, 100)
            x1_initial = 0
            x2_initial = 10

        # Позиции тел до столкновения
            x1 = x1_initial + v1 * t
            x2 = x2_initial - v2 * t

        # Создаем фигуру и оси
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.set_xlim(0, 2)
            ax.set_ylim(-1, 12)
            ax.set_title('Движение двух тел')
            ax.set_xlabel('Время (с)')
            ax.set_ylabel('Позиция (м)')
            ax.grid()

        # Создаем пустые линии для анимации
            line1, = ax.plot([], [], label='Первое тело', color='blue')
            line2, = ax.plot([], [], label='Второе тело', color='red')

        # Отметим момент столкновения
            collision_time = (x2_initial - x1_initial) / (v1 + v2)
            ax.axvline(x=collision_time, color='green',
                       linestyle='--', label='Столкновение')

            ax.legend()

        # Инициализация функции
            def init():
                line1.set_data([], [])
                line2.set_data([], [])
                return line1, line2

        # Функция обновления для анимации
            def update(frame):
                line1.set_data(t[:frame], x1[:frame])
                line2.set_data(t[:frame], x2[:frame])
                return line1, line2

            # Установите желаемую скорость (например, 50 мс между кадрами)
            speed = 100

        # Запускаем анимацию
            ani = animation.FuncAnimation(fig, update, frames=len(
                t), init_func=init, blit=True, repeat=False)
            plt.show()
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Пожалуйста, введите корректные числовые значения.")

    def visualize_collision(self):
        try:
            m1 = float(self.mass1_entry.get())
            v1 = float(self.velocity1_entry.get())
            m2 = float(self.mass2_entry.get())
            v2 = float(self.velocity2_entry.get())

            if not self.validate_inputs(m1, v1, m2, v2):
                return

            # Параметры для анимации
            x1_initial = 0
            x2_initial = 10
            x1 = x1_initial
            x2 = x2_initial

            # Создаем фигуру и оси
            fig, ax = plt.subplots()
            ax.set_xlim(-1, 12)
            ax.set_ylim(-1, 1)
            ax.set_aspect('equal')
            ax.set_facecolor('white')  # Устанавливаем белый фон
            ax.axis('off')  # Убираем оси

            # Создаем два шара
            ball1 = plt.Circle((x1, 0), 0.5, color='blue')
            ball2 = plt.Circle((x2, 0), 0.5, color='red')
            ax.add_artist(ball1)
            ax.add_artist(ball2)

            # Функция обновления для анимации
            def update(frame):
                nonlocal x1, x2, v1, v2
                # Обновляем позиции шаров
                x1 += v1 * 0.1
                x2 -= v2 * 0.1

                # Проверка на столкновение
                if x1 + 0.5 >= x2 - 0.5:  # Учитываем радиусы шаров
                    # Обработка столкновения (расчет новых скоростей)
                    v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
                    v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
                    v1, v2 = v1_final, v2_final  # Обновляем скорости после столкновения

                    # Перемещаем шары, чтобы они не пересекались
                    x1 = x2 - (0.5 + 0.5)  # Устанавливаем позицию первого шара

                    # Устанавливаем направление движения
                    if v1 > 0:
                        v1 = abs(v1)  # Первое тело движется вправо
                    else:
                        v1 = -abs(v1)  # Первое тело движется влево

                    if v2 > 0:
                        v2 = -abs(v2)  # Второе тело движется влево
                    else:
                        v2 = abs(v2)  # Второе тело движется вправо

                # Обновляем положение шаров
                ball1.center = (x1, 0)
                ball2.center = (x2, 0)

                return ball1, ball2

            # Запускаем анимацию
            ani = animation.FuncAnimation(
                fig, update, frames=np.arange(0, 100), interval=100)
            plt.show()

        except ValueError:
            messagebox.showerror(
                "Ошибка", "Пожалуйста, введите корректные числовые значения.")

    def example_collision_1(self):
        # Пример 1: Первое тело неподвижно, второе катится
        m1, m2 = 1, 1  # Массы
        v1, v2 = 3, 0  # Скорости

        self.run_collision_animation(m1, v1, m2, v2)

    def example_collision_2(self):
        # Пример 2: Оба тела движутся друг к другу
        m1, m2 = 1, 1  # Массы
        v1, v2 = 3, 3  # Скорости

        self.run_collision_animation(m1, v1, m2, v2)

    def example_collision_3(self):
        # Пример 3: Одно тело догоняет другое
        m1, m2 = 1, 1  # Массы
        v1, v2 = 3, 1  # Скорости

        self.run_collision_animation(m1, v1, m2, v2)

    def run_collision_animation(self, m1, v1, m2, v2):
        # Параметры для анимации
        x1_initial = 0
        x2_initial = 10
        x1 = x1_initial
        x2 = x2_initial

        # Создаем фигуру и оси
        fig, ax = plt.subplots()
        ax.set_xlim(-1, 12)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.set_facecolor('white')  # Устанавливаем белый фон
        ax.axis('off')  # Убираем оси

        # Создаем два шара
        ball1 = plt.Circle((x1, 0), 0.5, color='yellow')
        ball2 = plt.Circle((x2, 0), 0.5, color='red')
        ax.add_artist(ball1)
        ax.add_artist(ball2)

        # Функция обновления для анимации
        def update(frame):
            nonlocal x1, x2, v1, v2
            # Обновляем позиции шаров
            x1 += v1 * 0.1
            x2 -= v2 * 0.1

            # Проверка на столкновение
            if x1 + 0.5 >= x2 - 0.5:  # Учитываем радиусы шаров
                # Обработка столкновения (расчет новых скоростей)
                v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
                v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
                v1, v2 = v1_final, v2_final  # Обновляем скорости после столкновения

                # Перемещаем шары, чтобы они не пересекались
                x1 = x2 - (0.5 + 0.5)  # Устанавливаем позицию первого шара

                # Устанавливаем направление движения
                if v1 > 0:
                    v1 = abs(v1)  # Первое тело движется вправо
                else:
                    v1 = -abs(v1)  # Первое тело движется влево

                if v2 > 0:
                    v2 = -abs(v2)  # Второе тело движется влево
                else:
                    v2 = abs(v2)  # Второе тело движется вправо

            # Обновляем положение шаров
            ball1.center = (x1, 0)
            ball2.center = (x2, 0)

            return ball1, ball2

        # Запускаем анимацию
        ani = animation.FuncAnimation(
            fig, update, frames=np.arange(0, 100), interval=100)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImpulseLawApp(root)
    root.mainloop()
