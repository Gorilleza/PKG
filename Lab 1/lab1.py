import tkinter as tk
from tkinter import colorchooser, messagebox
import colorsys


def rgb_to_xyz(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    return (x * 100, y * 100, z * 100)


def xyz_to_rgb(x, y, z):
    x /= 100
    y /= 100
    z /= 100
    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252
    r, g, b = [max(0, min(255, int(c * 255))) for c in (r, g, b)]
    return r, g, b


def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def update_colors(event=None):
    try:
        r = int(entry_r.get())
        g = int(entry_g.get())
        b = int(entry_b.get())

        if any(c < 0 or c > 255 for c in (r, g, b)):
            raise ValueError("RGB values must be between 0 and 255.")

        color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')

        x, y, z = rgb_to_xyz(r, g, b)
        entry_x.delete(0, tk.END)
        entry_x.insert(0, f"{x:.2f}")
        entry_y.delete(0, tk.END)
        entry_y.insert(0, f"{y:.2f}")
        entry_z.delete(0, tk.END)
        entry_z.insert(0, f"{z:.2f}")

        h, s, v = rgb_to_hsv(r, g, b)
        entry_h.delete(0, tk.END)
        entry_h.insert(0, f"{h * 360:.2f}")
        entry_s.delete(0, tk.END)
        entry_s.insert(0, f"{s * 100:.2f}")
        entry_v.delete(0, tk.END)
        entry_v.insert(0, f"{v * 100:.2f}")

        # Update scales
        r_scale.set(r)
        g_scale.set(g)
        b_scale.set(b)
        x_scale.set(x)
        y_scale.set(y)
        z_scale.set(z)
        h_scale.set(h * 360)
        s_scale.set(s * 100)
        v_scale.set(v * 100)

    except ValueError as e:
        messagebox.showwarning("Ошибка", str(e))


def update_rgb_from_hsv(event=None):
    try:
        h = float(entry_h.get()) / 360
        s = float(entry_s.get()) / 100
        v = float(entry_v.get()) / 100

        r, g, b = hsv_to_rgb(h, s, v)

        entry_r.delete(0, tk.END)
        entry_r.insert(0, r)
        entry_g.delete(0, tk.END)
        entry_g.insert(0, g)
        entry_b.delete(0, tk.END)
        entry_b.insert(0, b)

        update_colors()

    except ValueError as e:
        messagebox.showwarning("Ошибка", str(e))


def choose_color():
    color_code = colorchooser.askcolor(title="Выберите цвет")[1]
    if color_code:
        r = int(color_code[1:3], 16)
        g = int(color_code[3:5], 16)
        b = int(color_code[5:7], 16)

        entry_r.delete(0, tk.END)
        entry_r.insert(0, r)
        entry_g.delete(0, tk.END)
        entry_g.insert(0, g)
        entry_b.delete(0, tk.END)
        entry_b.insert(0, b)

        update_colors()


def scale_update(val):
    entry_r.delete(0, tk.END)
    entry_r.insert(0, r_scale.get())
    entry_g.delete(0, tk.END)
    entry_g.insert(0, g_scale.get())
    entry_b.delete(0, tk.END)
    entry_b.insert(0, b_scale.get())
    update_colors()


def scale_update_hsv(val):
    entry_h.delete(0, tk.END)
    entry_h.insert(0, h_scale.get())
    entry_s.delete(0, tk.END)
    entry_s.insert(0, s_scale.get())
    entry_v.delete(0, tk.END)
    entry_v.insert(0, v_scale.get())
    update_rgb_from_hsv()


root = tk.Tk()
root.title("Color converter")
root.geometry("500x600")
root.resizable(False, False)

# RGB Scales
r_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=255, command=scale_update, length=200)
r_scale.grid(row=1, column=2)
g_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=255, command=scale_update, length=200)
g_scale.grid(row=2, column=2)
b_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=255, command=scale_update, length=200)
b_scale.grid(row=3, column=2)

# XYZ Scales
x_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, length=200)
x_scale.grid(row=5, column=2)
y_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, length=200)
y_scale.grid(row=6, column=2)
z_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, length=200)
z_scale.grid(row=7, column=2)

# HSV Scales
h_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=360, command=scale_update_hsv, length=200)
h_scale.grid(row=9, column=2)
s_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_hsv, length=200)
s_scale.grid(row=10, column=2)
v_scale = tk.Scale(orient=tk.HORIZONTAL, from_=0, to=100, command=scale_update_hsv, length=200)
v_scale.grid(row=11, column=2)

# Labels
tk.Label(root, text="R:").grid(row=1, column=0)
tk.Label(root, text="G:").grid(row=2, column=0)
tk.Label(root, text="B:").grid(row=3, column=0)
tk.Label(root, text="__________").grid(row=4, column=0)
tk.Label(root, text="X:").grid(row=5, column=0)
tk.Label(root, text="Y:").grid(row=6, column=0)
tk.Label(root, text="Z:").grid(row=7, column=0)
tk.Label(root, text="__________").grid(row=8, column=0)
tk.Label(root, text="H:").grid(row=9, column=0)
tk.Label(root, text="S:").grid(row=10, column=0)
tk.Label(root, text="V:").grid(row=11, column=0)

# Entry fields
entry_r = tk.Entry(root)
entry_g = tk.Entry(root)
entry_b = tk.Entry(root)
entry_x = tk.Entry(root)
entry_y = tk.Entry(root)
entry_z = tk.Entry(root)
entry_h = tk.Entry(root)
entry_s = tk.Entry(root)
entry_v = tk.Entry(root)

entry_r.grid(row=1, column=1)
entry_g.grid(row=2, column=1)
entry_b.grid(row=3, column=1)
entry_x.grid(row=5, column=1)
entry_y.grid(row=6, column=1)
entry_z.grid(row=7, column=1)
entry_h.grid(row=9, column=1)
entry_s.grid(row=10, column=1)
entry_v.grid(row=11, column=1)

# Set default values
r_scale.set(255)
g_scale.set(255)
b_scale.set(255)
h_scale.set(0)
s_scale.set(0)
v_scale.set(100)
x_scale.set(0)
y_scale.set(0)
z_scale.set(0)

color_display = tk.Frame(root, width=400, height=70)
color_display.grid(row=13, columnspan=3, pady=10, padx=50)
color_display.config(bg="#ffffff")

btn_choose_color = tk.Button(root, text="Choose color", command=choose_color)
btn_choose_color.grid(row=0, columnspan=3)

# Bindings
for entry in [entry_r, entry_g, entry_b]:
    entry.bind("<KeyRelease>", update_colors)

for entry in [entry_h, entry_s, entry_v]:
    entry.bind("<KeyRelease>", update_rgb_from_hsv)

root.mainloop() 
