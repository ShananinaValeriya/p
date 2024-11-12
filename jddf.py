from tkinter import ttk
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

        # Вкладка расчета параметров
        self.parameter_calculation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.parameter_calculation_tab, text='Расчет параметров')
        self.create_parameter_calculation_tab()

        # Вкладка графиков (по умолчанию отключена)
        self.graph_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text='Графики')
        self.create_graph_tab()
        self.notebook.tab(self.graph_tab, state='disabled')

        # Вкладка демонстрации (по умолчанию отключена)
        self.demo_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.demo_tab, text='Демонстрация')
        self.create_demo_tab()
        self.notebook.tab(self.demo_tab, state='disabled')

        # Вкладка примеров
        self.examples_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.examples_tab, text='Примеры')
        self.create_examples_tab()

    def create_theory_tab(self):
        theory_text = "Импульс (p) = масса (m) * скорость (v)\n" \
                      "Закон сохранения импульса гласит, что в замкнутой системе " \
                      "импульс сохраняется, если на систему не действуют внешние силы."
        theory_label = tk.Label(self.theory_tab, text=theory_text, justify='left', wraplength=400)
        theory_label.pack(padx=10, pady=10)

    def create_calculation_tab(self):
        self.mass1_label = tk.Label(self.calculation_tab, text="Масса первого тела (kg):")
        self.mass1_label.pack()
        self.mass1_entry = tk.Entry(self.calculation_tab)
        self.mass1_entry.pack()

        self.velocity1_label = tk.Label(self.calculation_tab, text="Скорость первого тела (m/s):")
        self.velocity1_label.pack()
        self.velocity1_entry = tk.Entry(self.calculation_tab)
        self.velocity1_entry.pack()

        self.mass2_label = tk.Label(self.calculation_tab, text="Масса второго тела (kg):")
        self.mass2_label.pack()
        self.mass2_entry = tk.Entry(self.calculation_tab)
        self.mass2_entry.pack()

        self.velocity2_label = tk.Label(self.calculation_tab, text="Скорость второго тела (m/s):")
        self.velocity2_label.pack()
        self.velocity2_entry = tk.Entry(self.calculation_tab)
        self.velocity2_entry.pack()

        self.calculate_button = tk.Button(self.calculation_tab, text="Рассчитать импульс", command=self.calculate_impulse)
        self.calculate_button.pack(pady=10)

        # Поле для отображения результатов
        self.result_label = tk.Label(self.calculation_tab, text="", wraplength=400)
        self.result_label.pack(pady=10)

    def create_parameter_calculation_tab(self):
        self.parameter_label = tk.Label(self.parameter_calculation_tab, text="Выберите тип взаимодействия:")
        self.parameter_label.pack(pady=10)

        self.interaction_var = tk.StringVar()
        self.interaction_dropdown = ttk.Combobox(self.parameter_calculation_tab, textvariable=self.interaction_var)
        self.interaction_dropdown['values'] = ("Абсолютно упругий удар", "Абсолютно неупругий удар")
        self.interaction_dropdown.pack(pady=10)
        self.interaction_dropdown.bind("<<ComboboxSelected>>", self.update_parameter_options)

        self.parameter_label = tk.Label(self.parameter_calculation_tab, text="Выберите параметр для расчета:")
        self.parameter_label.pack(pady=10)

        self.parameter_var = tk.StringVar()
        self.parameter_dropdown = ttk.Combobox(self.parameter_calculation_tab, textvariable=self.parameter_var)
        self.parameter_dropdown.pack(pady=10)
        self.parameter_dropdown.bind("<<ComboboxSelected>>", self.update_input_fields)

        self.input_frame = ttk.Frame(self.parameter_calculation_tab)
        self.input_frame.pack(pady=10)

        self.calculate_param_button = tk.Button(self.parameter_calculation_tab, text="Рассчитать", command=self.calculate_parameters)
        self.calculate_param_button.pack(pady=10)

        self.param_result_label = tk.Label(self.parameter_calculation_tab, text="", wraplength=400)
        self.param_result_label.pack(pady=10)

    def update_parameter_options(self, event):
        interaction_type = self.interaction_var.get()
        if interaction_type == "Абсолютно упругий удар":
            self.parameter_dropdown['values'] = (
                "Конечная скорость первого тела",
                "Конечная скорость второго тела",
                "Начальная скорость первого тела",
                "Начальная скорость второго тела",
                "Масса первого тела",
                "Масса второго тела"
            )
        elif interaction_type == "Абсолютно неупругий удар":
            self.parameter_dropdown['values'] = (
                "Конечная скорость обоих тел",
                "Начальная скорость первого тела",
                "Начальная скорость второго тела",
                "Масса первого тела",
                "Масса второго тела"
            )
        self.parameter_dropdown.set('')  # Сбросить выбор

    def update_input_fields(self, event):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
            
        selected_param = self.parameter_var.get()

        # В зависимости от выбранного параметра создаем соответствующие поля ввода
        if selected_param in ["Конечная скорость первого тела", "Конечная скорость второго тела"]:
            self.create_input_fields_for_final_velocity(selected_param)
        elif selected_param == "Конечная скорость обоих тел":
            self.create_input_fields_for_both_final_velocity()
        elif selected_param in ["Начальная скорость первого тела", "Начальная скорость второго тела", "Масса первого тела", "Масса второго тела"]:
            self.create_input_fields_for_initial_mass_or_velocity(selected_param)

    def create_input_fields_for_final_velocity(self, selected_param):
        
        if selected_param == "Конечная скорость первого тела":
            tk.Label(self.input_frame, text="Масса первого тела (kg):").pack()
            self.mass1_entry_param = tk.Entry(self.input_frame)
            self.mass1_entry_param.pack()

            tk.Label(self.input_frame, text="Скорость первого тела (m/s):").pack()
            self.velocity1_entry_param = tk.Entry(self.input_frame)
            self.velocity1_entry_param.pack()

            tk.Label(self.input_frame, text="Масса второго тела (kg):").pack()
            self.mass2_entry_param = tk.Entry(self.input_frame)
            self.mass2_entry_param.pack()

            tk.Label(self.input_frame, text="Скорость второго тела (m/s):").pack()
            self.velocity2_entry_param = tk.Entry(self.input_frame)
            self.velocity2_entry_param.pack()

            tk.Label(self.input_frame, text="Конечная скорость второго тела (m/s):").pack()
            self.final_velocity2_entry = tk.Entry(self.input_frame)
            self.final_velocity2_entry.pack()
            
        elif selected_param == "Конечная скорость второго тела":
            tk.Label(self.input_frame, text="Масса первого тела (kg):").pack()
            self.mass1_entry_param = tk.Entry(self.input_frame)
            self.mass1_entry_param.pack()

            tk.Label(self.input_frame, text="Скорость первого тела (m/s):").pack()
            self.velocity1_entry_param = tk.Entry(self.input_frame)
            self.velocity1_entry_param.pack()

            tk.Label(self.input_frame, text="Масса второго тела (kg):").pack()
            self.mass2_entry_param = tk.Entry(self.input_frame)
            self.mass2_entry_param.pack()

            tk.Label(self.input_frame, text="Скорость второго тела (m/s):").pack()
            self.velocity2_entry_param = tk.Entry(self.input_frame)
            self.velocity2_entry_param.pack()

            tk.Label(self.input_frame, text="Конечная скорость первого тела (m/s):").pack()
            self.final_velocity1_entry = tk.Entry(self.input_frame)
            self.final_velocity1_entry.pack()


    def create_input_fields_for_initial_mass_or_velocity(self, selected_param):
        if selected_param == "Начальная скорость первого тела":
            tk.Label(self.input_frame, text="Начальная скорость второго тела (m/s):").pack()
            self.initial_velocity2_entry = tk.Entry(self.input_frame)
            self.initial_velocity2_entry.pack()
            
            tk.Label(self.input_frame, text="Конечная скорость второго тела (m/s):").pack()
            self.final_velocity2_entry = tk.Entry(self.input_frame)
            self.final_velocity2_entry.pack()

            tk.Label(self.input_frame, text="Масса первого тела (kg):").pack()
            self.mass1_entry_param = tk.Entry(self.input_frame)
            self.mass1_entry_param.pack()

            tk.Label(self.input_frame, text="Конечная скорость первого тела (m/s):").pack()
            self.final_velocity1_entry = tk.Entry(self.input_frame)
            self.final_velocity1_entry.pack()

            tk.Label(self.input_frame, text="Масса второго тела (kg):").pack()
            self.mass2_entry_param = tk.Entry(self.input_frame)
            self.mass2_entry_param.pack()

        elif selected_param == "Начальная скорость второго тела":
            tk.Label(self.input_frame, text="Конечная скорость второго тела (m/s):").pack()
            self.final_velocity2_entry = tk.Entry(self.input_frame)
            self.final_velocity2_entry.pack()

            tk.Label(self.input_frame, text="Масса первого тела (kg):").pack()
            self.mass1_entry_param = tk.Entry(self.input_frame)
            self.mass1_entry_param.pack()

            tk.Label(self.input_frame, text="Конечная скорость первого тела (m/s):").pack()
            self.final_velocity1_entry = tk.Entry(self.input_frame)
            self.final_velocity1_entry.pack()

            tk.Label(self.input_frame, text="Начальная скорость первого тела (m/s):").pack()
            self.initial_velocity1_entry = tk.Entry(self.input_frame)
            self.initial_velocity1_entry.pack()

            tk.Label(self.input_frame, text="Масса второго тела (kg):").pack()
            self.mass2_entry_param = tk.Entry(self.input_frame)
            self.mass2_entry_param.pack()

        elif selected_param == "Масса первого тела":
            tk.Label(self.input_frame, text="Начальная скорость второго тела (m/s):").pack()
            self.initial_velocity2_entry = tk.Entry(self.input_frame)
            self.initial_velocity2_entry.pack()

            tk.Label(self.input_frame, text="Конечная скорость первого тела (m/s):").pack()
            self.final_velocity1_entry = tk.Entry(self.input_frame)
            self.final_velocity1_entry.pack()

            tk.Label(self.input_frame, text="Начальная скорость первого тела (m/s):").pack()
            self.initial_velocity1_entry = tk.Entry(self.input_frame)
            self.initial_velocity1_entry.pack()

            tk.Label(self.input_frame, text="Конечная скорость второго тела (m/s):").pack()
            self.final_velocity2_entry = tk.Entry(self.input_frame)
            self.final_velocity2_entry.pack()

            tk.Label(self.input_frame, text="Масса второго тела (kg):").pack()
            self.mass2_entry_param = tk.Entry(self.input_frame)
            self.mass2_entry_param.pack()

        elif selected_param == "Масса второго тела":
            tk.Label(self.input_frame, text="Начальная скорость второго тела (m/s):").pack()
            self.initial_velocity2_entry = tk.Entry(self.input_frame)
            self.initial_velocity2_entry.pack()

            tk.Label(self.input_frame, text="Конечная скорость первого тела (m/s):").pack()
            self.final_velocity1_entry = tk.Entry(self.input_frame)
            self.final_velocity1_entry.pack()
            
            tk.Label(self.input_frame, text="Начальная скорость первого тела (m/s):").pack()
            self.initial_velocity1_entry = tk.Entry(self.input_frame)
            self.initial_velocity1_entry.pack()

            tk.Label(self.input_frame, text="Конечная скорость второго тела (m/s):").pack()
            self.final_velocity2_entry = tk.Entry(self.input_frame)
            self.final_velocity2_entry.pack()

            tk.Label(self.input_frame, text="Масса первого тела (kg):").pack()
            self.mass1_entry_param = tk.Entry(self.input_frame)
            self.mass1_entry_param.pack()

    def calculate_parameters(self):
        selected_param = self.parameter_var.get()
        try:
            # Получаем значения из полей ввода
            m1 = float(self.mass1_entry_param.get()) if 'mass1_entry_param' in dir(self) else None
            m2 = float(self.mass2_entry_param.get()) if 'mass2_entry_param' in dir(self) else None
            v1 = float(self.velocity1_entry_param.get()) if 'velocity1_entry_param' in dir(self) else None
            v2 = float(self.velocity2_entry_param.get()) if 'velocity2_entry_param' in dir(self) else None
            v1_final = float(self.final_velocity1_entry.get()) if 'final_velocity1_entry' in dir(self) else None
            v2_final = float(self.final_velocity2_entry.get()) if 'final_velocity2_entry' in dir(self) else None

            # Печатаем значения для отладки
            print(f"m1: {m1}, m2: {m2}, v1: {v1}, v2: {v2}, v1_final: {v1_final}, v2_final: {v2_final}")

            # Проверяем, что все необходимые значения введены
            if selected_param == "Масса первого тела" and (m2 is None or v2 is None or v1 is None or v1_final is None):
                self.param_result_label.config(text="Ошибка: Необходимо ввести все параметры.")
                return

            if selected_param == "Масса второго тела" and (m1 is None or v1 is None or v2 is None or v2_final is None):
                self.param_result_label.config(text="Ошибка: Необходимо ввести все параметры.")
                return

            # Выполняем расчеты в зависимости от выбранного параметра
            if selected_param == "Конечная скорость первого тела":
                result = ((m2 * v2_final) + (m1 * v1) - (m2 * v2)) / m1
                self.param_result_label.config(text=f"Конечная скорость первого тела: {result:.2f} м/с")

            elif selected_param == "Конечная скорость второго тела":
                result = ((m1 * v1) - (m2 * v2) - (m1 * v1_final)) / m2
                self.param_result_label.config(text=f"Конечная скорость второго тела: {result:.2f} м/с")

            elif selected_param == "Масса первого тела":
                result = ((m2 * v2) - (m2 * v2_final)) / (v1_final - v1)
                self.param_result_label.config(text=f"Масса первого тела: {result:.2f} кг")

            elif selected_param == "Масса второго тела":
                result = (m1 * v1 - m1 * v1_final) / (v2_final - v2)
                self.param_result_label.config(text=f"Масса второго тела: {result:.2f} кг")

            elif selected_param == "Начальная скорость первого тела":
                result = (m1 * v1_final + m2 * v2_final - m2 * v2) / m1
                self.param_result_label.config(text=f"Начальная скорость первого тела: {result:.2f} м/с")

            elif selected_param == "Начальная скорость второго тела":
                result = (m2 * v2_final + m1 * v1_final - m1 * v1) / m2
                self.param_result_label.config(text=f"Начальная скорость второго тела: {result:.2f} м/с")
        
        except Exception as e:
            self.param_result_label.config(text="Ошибка: " + str(e))



    def create_graph_tab(self):
        self.graph_button = tk.Button(self.graph_tab, text="Построить график", command=self.visualize_graph)
        self.graph_button.pack(pady=10)

    def create_demo_tab(self):
        self.demo_button = tk.Button(self.demo_tab, text="Демонстрация столкновения", command=self.visualize_collision)
        self.demo_button.pack(pady=10)

    def create_examples_tab(self):
        self.example1_button = tk.Button(self.examples_tab, text="Пример 1", command=self.example_collision_1)
        self.example1_button.pack(pady=10)

        self.example2_button = tk.Button(self.examples_tab, text="Пример 2", command=self.example_collision_2)
        self.example2_button.pack(pady=10)

    def validate_inputs(self, m1, v1, m2, v2):
        if m1 <= 0:
            messagebox.showerror("Ошибка", "Масса первого тела должна быть положительной и не равной нулю.")
            return False
        if m2 <= 0:
            messagebox.showerror("Ошибка", "Масса второго тела должна быть положительной и не равной нулю.")
            return False
        if v1 < 0:
            messagebox.showerror("Ошибка", "Скорость первого тела не может быть отрицательной.")
            return False
        if v2 < 0:
            messagebox.showerror("Ошибка", "Скорость второго тела не может быть отрицательной.")
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
            self.result_label.config(text=result_text)

            # Активируем вкладки графиков и демонстрации
            self.notebook.tab(self.graph_tab, state='normal')
            self.notebook.tab(self.demo_tab, state='normal')

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения.")

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
        m1, m2 = 2, 2  # Массы для первого примера
        v1, v2 = 4, 4  # Первое тело неподвижно, второе движется

        self.run_collision_animation1(m1, v1, m2, v2)

    def example_collision_2(self):
        m3, m4 = 3, 2  # Массы для второго примера
        v3, v4 = 2, 3  # Шар с большим размером движется к меньшему

        self.run_collision_animation2(m3, v3, m4, v4)

    def run_collision_animation1(self, m1, v1, m2, v2):
        x1_initial = 0
        x2_initial = 10
        x1 = x1_initial
        x2 = x2_initial

        fig, ax = plt.subplots()
        ax.set_xlim(-1, 12)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.set_facecolor('white')
        ax.axis('off')

        ball1 = plt.Circle((x1, 0), 0.5, color='yellow')
        ball2 = plt.Circle((x2, 0), 0.5, color='red')
        ax.add_artist(ball1)
        ax.add_artist(ball2)

        def update(frame):
            nonlocal x1, x2, v1, v2
            x1 += v1 * 0.1
            x2 -= v2 * 0.1

            if x1 + 0.5 >= x2 - 0.5:
                v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
                v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
                v1, v2 = v1_final, v2_final
                x1 = x2 - (0.5 + 0.5)

                if v1 > 0:
                    v1 = abs(v1)
                else:
                    v1 = -abs(v1)

                if v2 > 0:
                    v2 = -abs(v2)
                else:
                    v2 = abs(v2)

            # Проверка на выход за границы
            if x1 < -1 or x1 > 12 or x2 < -1 or x2 > 12:
                # Сброс позиций и скоростей
                x1, x2 = x1_initial, x2_initial
                v1, v2 = 4, 4  # Можно задать начальные скорости заново

            ball1.center = (x1, 0)
            ball2.center = (x2, 0)

            return ball1, ball2

        ani = animation.FuncAnimation(
            fig, update, frames=np.arange(0, 100), interval=100)
        plt.show()

    def run_collision_animation2(self, m3, v3, m4, v4):
        x3_initial = 0
        x4_initial = 10
        x3 = x3_initial
        x4 = x4_initial

        fig, ax = plt.subplots()
        ax.set_xlim(-1, 12)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.set_facecolor('white')
        ax.axis('off')

        ball3 = plt.Circle((x3, 0), 0.4, color='blue')
        ball4 = plt.Circle((x4, 0), 0.5, color='green')
        ax.add_artist(ball3)
        ax.add_artist(ball4)

        def calculate_velocities(m3, v3, m4, v4):
            v_final = (m3 * v3 + m4 * v4) / (m3 + m4)
            return v_final, v_final

        def update(frame):
            nonlocal x3, x4, v3, v4
            x3 += v3 * 0.1
            x4 -= v4 * 0.1

            if x3 + 0.3 >= x4 - 0.5:
                v_final = calculate_velocities(m3, v3, m4, v4)
                v3 = v_final[0]
                v4 = v_final[0]
                x3 = x4 - (0.3 + 0.5)

            if x3 < -1 or x3 > 12 or x4 < -1 or x4 > 12:
                # Сброс позиций и скоростей
                x3, x4 = x3_initial, x4_initial
                v3, v4 = 2, 3

            ball3.center = (x3, 0)
            ball4.center = (x4, 0)

            return ball3, ball4

        ani = animation.FuncAnimation(
            fig, update, frames=np.arange(0, 100), interval=100)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImpulseLawApp(root)
    root.mainloop()
