import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
import time
import math

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint Pro")
        self.root.geometry("1000x720")

        # === Drawing variables ===
        self.old_x = None
        self.old_y = None
        self.last_time = None
        self.speed = 0
        self.pen_width = 3
        self.pen_color = '#000000'
        self.mode = 'draw'  # or 'erase'
        self.preview_line = None
        self.bg_color = 'white'
        self.canvas_fg = 'white'

        self.COLOR_NAMES = {
            "#000000": "Black", "#808080": "Gray", "#C0C0C0": "Silver", "#FFFFFF": "White",
            "#800000": "Maroon", "#FF0000": "Red", "#808000": "Olive", "#FFFF00": "Yellow",
            "#008000": "Green", "#00FF00": "Lime", "#008080": "Teal", "#00FFFF": "Cyan",
            "#000080": "Navy", "#0000FF": "Blue", "#800080": "Purple", "#FF00FF": "Magenta",
            "#A52A2A": "Brown", "#FFA500": "Orange", "#F5DEB3": "Wheat", "#DC143C": "Crimson"
        }

        self.setup_ui()

    def setup_ui(self):
        # === Canvas ===
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, width=1000, height=600, cursor="cross")
        self.canvas.pack()

        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<Motion>', self.track_mouse)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        # === Control Panel ===
        control = tk.Frame(self.root)
        control.pack(pady=4)

        for color in self.COLOR_NAMES:
            btn = tk.Button(control, bg=color, width=2, command=lambda col=color: self.set_color(col))
            btn.pack(side=tk.LEFT, padx=1)

        # Pen width slider
        self.slider = tk.Scale(control, from_=1, to=20, orient=tk.HORIZONTAL,
                               showvalue=0, length=100, width=8, sliderlength=10,
                               troughcolor="#ddd", bd=0, highlightthickness=0,
                               command=lambda val: self.update_status())
        self.slider.set(self.pen_width)
        self.slider.pack(side=tk.LEFT, padx=10)

        # Eraser toggle
        eraser_btn = tk.Button(control, text="🧽 Eraser", command=self.toggle_eraser)
        eraser_btn.pack(side=tk.LEFT, padx=5)

        # Clear button
        clear_btn = tk.Button(control, text="🗑 Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Save button
        save_btn = tk.Button(control, text="💾 Save", command=self.save_drawing)
        save_btn.pack(side=tk.LEFT, padx=5)

        # Theme toggle
        theme_btn = tk.Button(control, text="🌓 Toggle Theme", command=self.toggle_theme)
        theme_btn.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status = tk.Label(self.root, text="", anchor='w', font=("Arial", 9), fg="gray")
        self.status.pack(fill=tk.X)

        self.update_status()

    def set_color(self, col):
        self.pen_color = col
        self.mode = 'draw'
        self.update_status()

    def toggle_eraser(self):
        self.mode = 'erase' if self.mode != 'erase' else 'draw'
        self.update_status()

    def toggle_theme(self):
        if self.bg_color == 'white':
            self.bg_color = '#2b2b2b'
            self.canvas_fg = 'black'
        else:
            self.bg_color = 'white'
            self.canvas_fg = 'white'
        self.canvas.config(bg=self.bg_color)
        self.clear_canvas(redraw=False)
        self.update_status()

    def draw(self, event):
        self.pen_width = self.slider.get()

        color = self.bg_color if self.mode == 'erase' else self.pen_color

        if self.old_x and self.old_y:
            self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                fill=color, width=self.pen_width,
                capstyle=tk.ROUND, smooth=True
            )

            dist = math.sqrt((event.x - self.old_x) ** 2 + (event.y - self.old_y) ** 2)
            t = time.time()
            if self.last_time:
                dt = t - self.last_time
                if dt > 0:
                    self.speed = dist / dt
            self.last_time = t

        self.old_x = event.x
        self.old_y = event.y
        self.update_status()

        # Line preview
        if self.preview_line:
            self.canvas.delete(self.preview_line)
        self.preview_line = self.canvas.create_line(
            self.old_x, self.old_y, event.x, event.y,
            fill=self.pen_color, width=1, dash=(2, 2)
        )

    def reset(self, event):
        self.old_x = None
        self.old_y = None
        self.last_time = None
        self.speed = 0
        if self.preview_line:
            self.canvas.delete(self.preview_line)
            self.preview_line = None
        self.update_status()

    def clear_canvas(self, redraw=True):
        self.canvas.delete("all")
        if redraw:
            self.update_status()

    def save_drawing(self):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        img = ImageGrab.grab().crop((x, y, x1, y1))
        file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file:
            img.save(file)

    def track_mouse(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.update_status()

    def update_status(self):
        color_name = self.COLOR_NAMES.get(self.pen_color.upper(), "Custom")
        mode_icon = "✏️" if self.mode == 'draw' else "🧽"
        status = f"{mode_icon} Mode | 🎨 {color_name} ({self.pen_color.upper()}) | ✏️ Width: {self.pen_width} | 🏃 Speed: {self.speed:.2f} px/s | 🖱 {getattr(self, 'mouse_x', 0)}, {getattr(self, 'mouse_y', 0)}"
        self.status.config(text=status)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
