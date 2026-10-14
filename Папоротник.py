import random
import tkinter as tk
from tkinter import ttk


PRESETS = {
    "Классический": (0.04, 1.00, 0.85),
    "Узкий": (0.02, 0.60, 0.88),
    "Широкий": (0.04, 1.45, 0.80),
    "Изогнутый": (-0.12, 1.10, 0.85),
    "Высокий": (0.03, 0.85, 0.91),
}

WIDTH, HEIGHT = 660, 650
sliders = {}
after_id = None


def generate_points(count, bend, spread, height):
    x = y = 0.0
    rng = random.Random(42)
    points = []

    for i in range(count + 20):
        r = rng.random()
        if r < 0.01:
            x, y = 0, 0.16 * y
        elif r < 0.86:
            x, y = 0.85 * x + bend * y, -bend * x + height * y + 1.6
        elif r < 0.93:
            x, y = 0.20 * x - 0.26 * spread * y, 0.23 * x + 0.22 * y + 1.6
        else:
            x, y = -0.15 * x + 0.28 * spread * y, 0.26 * x + 0.24 * y + 0.44

        if i >= 20:
            points.append((x, y))

    return points


def draw():
    global after_id
    after_id = None
    bend = sliders["Изгиб"].get()
    spread = sliders["Ширина"].get()
    height = sliders["Высота"].get()
    count = sliders["Точки"].get()
    points = generate_points(count, bend, spread, height)

    xs, ys = zip(*points)
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    scale = min(610 / max(x_max - x_min, 0.001),
                600 / max(y_max - y_min, 0.001))
    dx = (WIDTH - (x_max - x_min) * scale) / 2
    dy = (HEIGHT - (y_max - y_min) * scale) / 2

    canvas.delete("all")
    for x, y in points:
        px = round(dx + (x - x_min) * scale)
        py = round(dy + (y_max - y) * scale)
        canvas.create_rectangle(px, py, px + 1, py + 1,
                                fill="#68ef8c", outline="")

    status.config(text=f"Точек: {count}   b={bend:.2f}   w={spread:.2f}   d={height:.2f}")


def update(_=None):
    global after_id
    if after_id is not None:
        root.after_cancel(after_id)
    after_id = root.after(180, draw)


def select_preset(_=None):
    for name, value in zip(("Изгиб", "Ширина", "Высота"), PRESETS[choice.get()]):
        sliders[name].set(value)
    update()


def reset():
    choice.set("Классический")
    select_preset()


def main():
    global root, canvas, status, choice
    root = tk.Tk()
    root.title("Папоротник Барнсли")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()
    canvas = tk.Canvas(frame, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
    canvas.pack(side=tk.LEFT)
    panel = tk.Frame(frame, padx=12)
    panel.pack(side=tk.LEFT, anchor="n")

    tk.Label(panel, text="Папоротник Барнсли", font=("Arial", 14, "bold")).pack(pady=10)

    settings = (
        ("Изгиб", -0.17, 0.17, 0.01, 0.04),
        ("Ширина", 0.50, 1.55, 0.05, 1.00),
        ("Высота", 0.75, 0.92, 0.01, 0.85),
        ("Точки", 2000, 50000, 1000, 20000),
    )
    for name, start, end, step, value in settings:
        scale = tk.Scale(panel, label=name, from_=start, to=end, resolution=step,
                         orient=tk.HORIZONTAL, length=230, command=update)
        scale.set(value)
        scale.pack()
        sliders[name] = scale

    tk.Label(panel, text="Вариант растения").pack(pady=(15, 0))
    choice = ttk.Combobox(panel, values=list(PRESETS), state="readonly", width=22)
    choice.set("Классический")
    choice.pack(pady=5)
    choice.bind("<<ComboboxSelected>>", select_preset)
    tk.Button(panel, text="Сбросить настройки", command=reset).pack(pady=10)

    status = tk.Label(root, anchor="w", padx=10)
    status.pack(fill=tk.X)
    root.after(100, draw)
    root.mainloop()


if __name__ == "__main__":
    main()
