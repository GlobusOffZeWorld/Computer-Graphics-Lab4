import matplotlib.pyplot as plt
import time
import numpy as np
import tkinter as tk
from tkinter import messagebox

# глобальные переменные
global x1, y1, x2, y2, scale, radius
x1 = y1 = x2 = y2 = scale = radius = 0.0


def ok_button_click():
    global x1, y1, x2, y2, scale, radius
    try:
        x1 = int(x1_entry.get())
        y1 = int(y1_entry.get())
        x2 = int(x2_entry.get())
        y2 = int(y2_entry.get())
        scale = int(scale_entry.get())
        radius = int(radius_entry.get())
        if not all(isinstance(val, (int, float)) for val in (x1, y1, x2, y2, scale, radius)):
            raise ValueError("Все значения должны быть числами")
        if not all(val < scale for val in (x1, y1, x2, y2, radius)):
            raise ValueError("Значения должны быть меньше scale")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))
        return
    else:
        # закрываем диалоговое окно
        root.destroy()


# создаем главное окно
root = tk.Tk()
root.title("Диалоговое окно")

# создаем поля ввода
x1_label = tk.Label(root, text="x1:")
x1_label.grid(row=0, column=0)
x1_entry = tk.Entry(root)
x1_entry.grid(row=0, column=1)

y1_label = tk.Label(root, text="y1:")
y1_label.grid(row=1, column=0)
y1_entry = tk.Entry(root)
y1_entry.grid(row=1, column=1)

x2_label = tk.Label(root, text="x2:")
x2_label.grid(row=2, column=0)
x2_entry = tk.Entry(root)
x2_entry.grid(row=2, column=1)

y2_label = tk.Label(root, text="y2:")
y2_label.grid(row=3, column=0)
y2_entry = tk.Entry(root)
y2_entry.grid(row=3, column=1)

scale_label = tk.Label(root, text="scale:")
scale_label.grid(row=4, column=0)
scale_entry = tk.Entry(root)
scale_entry.grid(row=4, column=1)

radius_label = tk.Label(root, text="radius:")
radius_label.grid(row=5, column=0)
radius_entry = tk.Entry(root)
radius_entry.grid(row=5, column=1)

# создаем кнопку "ОК"
ok_button = tk.Button(root, text="OK", command=ok_button_click)
ok_button.grid(row=6, column=1)

root.mainloop()

SIZE = int(scale)
WINDOW_SIZE = 10
f, ax = plt.subplots(2, 2, figsize=(WINDOW_SIZE, WINDOW_SIZE))



def draw_step_by_step(x1, y1, x2, y2):
    ax[0, 0].set_xlim([0, SIZE])
    ax[0, 0].set_ylim([0, SIZE])
    ax[0, 0].set_title('Пошаговый алгоритм')
    # f.suptitle('Пошаговый алгоритм')
    f.show()
    k = (y2 - y1)
    if (x2 - x1) != 0:
        k = (y2 - y1)/(x2 - x1)

    b = y2 - k * x2
    dx = abs(x2 - x1)/(max(abs(x2 - x1), abs(y2 - y1) * 2))
    if (x2 > x1):
        dx = dx
    else:
        dx = -dx

    x = x1
    y = k * x + b
    img = np.zeros((SIZE, SIZE))
    begin = time.time()
    while x < x2:
        img[int(y), int(x)] = 1
        y = k * x + b
        x = x + dx
    end = time.time()
    ax[0, 0].imshow(img, cmap='binary')
    print('Time spent: {}'.format(end - begin))
    return 'Time spent: {}'.format(end - begin)


def draw_dda(x1, y1, x2, y2):
    # f, ax = plt.subplots(figsize=(WINDOW_SIZE, WINDOW_SIZE))
    ax[0, 1].set_xlim([0, SIZE])
    ax[0, 1].set_ylim([0, SIZE])
    ax[0, 1].set_title('Алгоритм ЦДА')
    f.show()
    dx = x2 - x1
    dy = y2 - y1

    if dx > dy:
        steps = dx
    else:
        steps = dy

    x_increment = dx / steps
    y_increment = dy / steps
    img = np.zeros((SIZE, SIZE))
    begin = time.time()
    for i in range(int(steps)):
        img[int(y1), int(x1)] = 1
        x1 = x1 + x_increment
        y1 = y1 + y_increment
    end = time.time()
    ax[0, 1].imshow(img, cmap='binary')

    print('Time spent: {}'.format(end - begin))
    return 'Time spent: {}'.format(end - begin)


def draw_bresenham(x1, y1, x2, y2):
    # f, ax = plt.subplots(figsize=(WINDOW_SIZE, WINDOW_SIZE))
    ax[1, 0].set_xlim([0, SIZE])
    ax[1, 0].set_ylim([0, SIZE])
    ax[1, 0].set_title('Алгоритм Брезенхема')

    # f.suptitle('Алгоритм Брезенхема')
    f.show()

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    x = x1
    y = y1

    img = np.zeros((SIZE, SIZE))
    img[int(y), int(x)] = 1
    begin = time.time()
    while x != x2 or y != y2:
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        img[int(y), int(x)] = 1
    end = time.time()

    ax[1, 0].imshow(img, cmap='binary')
    print('Time spent: {}'.format(end - begin))
    return 'Time spent: {}'.format(end - begin)


def draw_circle_bresenham(xc, yc, r):
    # f, ax = plt.subplots(figsize=(WINDOW_SIZE, WINDOW_SIZE))
    ax[1, 1].set_xlim([-SIZE, SIZE])
    ax[1, 1].set_ylim([-SIZE, SIZE])
    ax[1, 1].set_title('Алгоритм Брезенхема(для окружности)')
    
    # f.suptitle('Алгоритм Брезенхема(для окружности)')
    f.show()

    x = 0
    y = r
    d = 3 - 2 * r

    img = np.zeros((2 * SIZE, 2 * SIZE))
    begin = time.time()

    while y >= x:
        img[SIZE + xc + x, SIZE + yc + y] = 1
        img[SIZE + xc + x, SIZE + yc - y] = 1
        img[SIZE + xc - x, SIZE + yc + y] = 1
        img[SIZE + xc - x, SIZE + yc - y] = 1
        img[SIZE + xc + y, SIZE + yc + x] = 1
        img[SIZE + xc + y, SIZE + yc - x] = 1
        img[SIZE + xc - y, SIZE + yc + x] = 1
        img[SIZE + xc - y, SIZE + yc - x] = 1
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
    end = time.time()

    ax[1, 1].imshow(img,  cmap='binary', extent=(-SIZE,
              img.shape[1]-SIZE, -SIZE, img.shape[0]-SIZE))
    print('Time spent: {}'.format(end - begin))
    return 'Time spent: {}'.format(end - begin)


def main():

    time_1 = draw_step_by_step(x1, y1, x2, y2)
    time_2 = draw_dda(x1, y1, x2, y2)
    time_3 = draw_bresenham(x1, y1, x2, y2)
    time_4 = draw_circle_bresenham(x1, y1, radius)

    input()

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(f"Message", f"{time_1}\n{time_2}\n{time_3}\n{time_4}")

    # запускаем главный цикл


if __name__ == '__main__':
    main()
