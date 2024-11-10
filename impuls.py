import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


class ImpulseLawApp:
    def __init__(self, master):
        self.master = master
        master.title("Закон сохранения импульса")

        self.label = tk.Label(master, text="Закон сохранения импульса")
        self.label.pack()

        self.info = tk.Label(
            master, text="Импульс (p) = масса (m) * скорость (v)")
        self.info.pack()

        self.mass1_label = tk.Label(master, text="Масса первого тела (kg):")
        self.mass1_label.pack()
        self.mass1_entry = tk.Entry(master)
        self.mass1_entry.pack()

        self.velocity1_label = tk.Label(
            master, text="Скорость первого тела (m/s):")
        self.velocity1_label.pack()
        self.velocity1_entry = tk.Entry(master)
        self.velocity1_entry.pack()

        self.mass2_label = tk.Label(master, text="Масса второго тела (kg):")
        self.mass2_label.pack()
        self.mass2_entry = tk.Entry(master)
        self.mass2_entry.pack()

        self.velocity2_label = tk.Label(
            master, text="Скорость второго тела (m/s):")
        self.velocity2_label.pack()
        self.velocity2_entry = tk.Entry(master)
        self.velocity2_entry.pack()

        self.calculate_button = tk.Button(
            master, text="Рассчитать импульс", command=self.calculate_impulse)
        self.calculate_button.pack()

        self.visualize_button = tk.Button(
            master, text="Демонстрация столкновения", command=self.visualize_collision)
        self.visualize_button.pack()

    def calculate_impulse(self):
        try:
            m1 = float(self.mass1_entry.get())
            v1 = float(self.velocity1_entry.get())
            m2 = float(self.mass2_entry.get())
            v2 = float(self.velocity2_entry.get())

            impulse1 = m1 * v1
            impulse2 = m2 * v2

            total_impulse = impulse1 + impulse2

            messagebox.showinfo("Результат", f"Импульс первого тела: {impulse1} kg*m/s\n"
                                f"Импульс второго тела: {impulse2} kg*m/s\n"
                                f"Общий импульс: {total_impulse} kg*m/s")
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Пожалуйста, введите корректные числовые значения.")

    def visualize_collision(self):
        try:
            m1 = float(self.mass1_entry.get())
            v1 = float(self.velocity1_entry.get())
            m2 = float(self.mass2_entry.get())
            v2 = float(self.velocity2_entry.get())

            # Параметры для графика
            t = np.linspace(0, 2, 100)
            x1_initial = 0
            x2_initial = 10

            # Позиции тел до столкновения
            x1 = x1_initial + v1 * t
            x2 = x2_initial - v2 * t

            plt.figure(figsize=(10, 5))
            plt.plot(t, x1, label='Первое тело', color='blue')
            plt.plot(t, x2, label='Второе тело', color='red')

            # Отметим момент столкновения
            collision_time = (x2_initial - x1_initial) / (v1 + v2)
            plt.axvline(x=collision_time, color='green',
                        linestyle='--', label='Столкновение')

            plt.title('Движение двух тел')
            plt.xlabel('Время (с)')
            plt.ylabel('Позиция (м)')
            plt.legend()
            plt.grid()
            plt.show()
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Пожалуйста, введите корректные числовые значения.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImpulseLawApp(root)
    root.mainloop()
