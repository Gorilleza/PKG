import tkinter as tk
from tkinter import ttk
import time

class RasterGraphicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Растровые алгоритмы с координатной сеткой")
        self.grid_step = 40
        self.grid_range = 15
        self.create_interface()
        self.canvas_size = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=12, padx=10, pady=10)
        self.draw_grid()

    def create_interface(self):
        ttk.Label(self.root, text="Выберите алгоритм:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.algorithm = tk.StringVar(value="dda")
        ttk.Combobox(
            self.root,
            textvariable=self.algorithm,
            values=["dda", "bresenham_line", "bresenham_circle", "step_by_step"],
            state="readonly",
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Начальная точка (x1, y1):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.x1_entry = ttk.Entry(self.root, width=5)
        self.x1_entry.grid(row=0, column=3, padx=2, pady=5)
        self.y1_entry = ttk.Entry(self.root, width=5)
        self.y1_entry.grid(row=0, column=4, padx=2, pady=5)

        ttk.Label(self.root, text="Конечная точка (x2, y2) / Радиус:").grid(row=0, column=5, padx=5, pady=5, sticky="e")
        self.x2_entry = ttk.Entry(self.root, width=5)
        self.x2_entry.grid(row=0, column=6, padx=2, pady=5)
        self.y2_entry = ttk.Entry(self.root, width=5)
        self.y2_entry.grid(row=0, column=7, padx=2, pady=5)

        ttk.Button(self.root, text="Построить", command=self.run_algorithm).grid(row=0, column=8, padx=10, pady=5)

        self.time_label = ttk.Label(self.root, text="Время выполнения: ---")
        self.time_label.grid(row=2, column=0, columnspan=12, padx=10, pady=5, sticky="w")

        ttk.Label(self.root, text="Масштаб сетки:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.grid_scale = tk.Scale(self.root, from_=15, to_=80, orient="horizontal", command=self.update_grid_step)
        self.grid_scale.set(self.grid_step)  # Установить начальный шаг
        self.grid_scale.grid(row=3, column=1, padx=5, pady=5)

    def draw_grid(self):
        self.canvas.delete("all")
        step = self.grid_step
        grid_range = self.grid_range
        canvas_mid = self.canvas_size // 2

        for i in range(-grid_range, grid_range + 1):
            coord = canvas_mid + i * step
            self.canvas.create_line(coord, 0, coord, self.canvas_size, fill="#ddd")
            self.canvas.create_line(0, coord, self.canvas_size, coord, fill="#ddd")

            if i != 0:
                self.canvas.create_text(coord, canvas_mid + 15, text=str(i), fill="black")
                self.canvas.create_text(canvas_mid - 15, coord, text=str(-i), fill="black")

        self.canvas.create_line(canvas_mid, 0, canvas_mid, self.canvas_size, width=2, arrow=tk.LAST)
        self.canvas.create_line(0, canvas_mid, self.canvas_size, canvas_mid, width=2, arrow=tk.LAST)
        self.canvas.create_text(canvas_mid + 20, canvas_mid - 10, text="0", fill="black")

    def to_canvas_coordinates(self, x, y):
        step = self.grid_step
        grid_range = self.grid_range
        canvas_mid = self.canvas_size // 2
        canvas_x = canvas_mid + x * step
        canvas_y = canvas_mid - y * step
        return canvas_x, canvas_y

    def draw_pixel(self, x, y, color="black"):
        canvas_x, canvas_y = self.to_canvas_coordinates(x, y)
        self.canvas.create_rectangle(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill=color, outline=color)

    def dda_algorithm(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps
        x, y = x1, y1
        for _ in range(steps + 1):
            self.draw_pixel(round(x), round(y))
            x += x_increment
            y += y_increment

    def bresenham_line(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_pixel(x1, y1)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def bresenham_circle(self, xc, yc, r):
        x, y = 0, r
        d = 3 - 2 * r
        self.draw_circle_points(xc, yc, x, y)
        while y >= x:
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            self.draw_circle_points(xc, yc, x, y)

    def draw_circle_points(self, xc, yc, x, y):
        points = [(x, y), (y, x), (-x, y), (-y, x),
                  (-x, -y), (-y, -x), (x, -y), (y, -x)]
        for px, py in points:
            self.draw_pixel(xc + px, yc + py)

    def step_by_step(self, x1, y1, x2, y2):
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else 0
        y = y1
        for x in range(x1, x2 + 1):
            self.draw_pixel(x, round(y))
            y += slope

    def run_algorithm(self):
        self.draw_grid()
        algorithm = self.algorithm.get()
        x1 = int(self.x1_entry.get())
        y1 = int(self.y1_entry.get())
        x2 = int(self.x2_entry.get())
        y2 = int(self.y2_entry.get())

        start_time = time.time()

        if algorithm == "dda":
            self.dda_algorithm(x1, y1, x2, y2)
        elif algorithm == "bresenham_line":
            self.bresenham_line(x1, y1, x2, y2)
        elif algorithm == "bresenham_circle":
            self.bresenham_circle(x1, y1, x2)
        elif algorithm == "step_by_step":
            self.step_by_step(x1, y1, x2, y2)

        end_time = time.time()
        elapsed_time = end_time - start_time

        self.time_label.config(text=f"Время выполнения: {elapsed_time:.6f} секунд")

    def update_grid_step(self, val):
        self.grid_step = int(val)
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = RasterGraphicsApp(root)
    root.mainloop()
