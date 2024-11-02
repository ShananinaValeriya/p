import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


def calculate_momentum():
    try:
        m1 = float(entry_m1.get())  # Масса первого тела
        v1 = float(entry_v1.get())  # Скорость первого тела
        m2 = float(entry_m2.get())  # Масса второго тела
        v2 = float(entry_v2.get())  # Скорость второго тела

        # Начальный импульс
        initial_momentum = m1 * v1 + m2 * v2

        # Применение закона сохранения импульса: финальная скорость тандемного тела
        final_velocity = (m1 * v1 + m2 * v2) / (m1 + m2)
        final_momentum = (m1 + m2) * final_velocity

        # Проверка сохранения импульса
        if np.isclose(initial_momentum, final_momentum):
            result = f'Импульс сохранён:\\nНачальный импульс: {initial_momentum:.2f}\\nКонечный импульс: {final_momentum:.2f}'
        else:
            result = 'Ошибка в расчётах!'

        messagebox.showinfo("Результат", result)

        # Визуализация
        visualize(m1, v1, m2, v2, final_velocity)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения!")


def visualize(m1, v1, m2, v2, final_velocity):
    plt.figure(figsize=(10, 5))

    # Названия объектов
    objects = ['Тело 1', 'Тело 2', 'Тело 1+2 после']
    masses = [m1, m2, m1 + m2]  # Массы тел
    velocities = [v1, v2, final_velocity]  # Скорости

    # Создание столбцов на графике
    x = np.arange(len(objects))

    # Столбчатая диаграмма
    plt.bar(x - 0.2, masses, 0.4, label='Масса', alpha=0.6, color='blue')
    plt.bar(x + 0.2, velocities, 0.4, label='Скорость',
            alpha=0.6, color='orange')

    plt.xlabel('Объекты')
    plt.ylabel('Значения')
    plt.title('Закон сохранения импульса')
    plt.xticks(x, objects)
    plt.legend()
    plt.grid(axis='y')
    plt.show()


# Создание графического интерфейса
root = tk.Tk()
root.title("Закон сохранения импульса")

tk.Label(root, text="Масса тела 1 (кг):").grid(row=0)
tk.Label(root, text="Скорость тела 1 (м/с):").grid(row=1)
tk.Label(root, text="Масса тела 2 (кг):").grid(row=2)
tk.Label(root, text="Скорость тела 2 (м/с):").grid(row=3)

# Поля ввода
entry_m1 = tk.Entry(root)
entry_v1 = tk.Entry(root)
entry_m2 = tk.Entry(root)
entry_v2 = tk.Entry(root)

entry_m1.grid(row=0, column=1)
entry_v1.grid(row=1, column=1)
entry_m2.grid(row=2, column=1)
entry_v2.grid(row=3, column=1)

# Кнопка для вычисления
tk.Button(root, text="Рассчитать", command=calculate_momentum).grid(
    row=4, columnspan=2)

root.mainloop()
