import tkinter as tk
from tkinter import colorchooser, filedialog
import time
import math
from PIL import Image, ImageDraw, ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint App")
        self.root.geometry("1000x700")

        # Drawing canvas
        self.canvas = tk.Canvas(self.root, bg='white', width=1000, height=600)
        self.canvas.pack()

        # Drawing attributes
        self.old_x = None
        self.old_y = None
        self.pen_width = 3
        self.pen_color = 'black'
        self.last_time = None
        self.speed = 0

        # Bindings
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        # UI Controls
        self.create_ui()

        # Status bar
        self.status = tk.Label(self.root, text="", anchor='w', font=("Arial", 9), fg="gray")
        self.status.pack(fill=tk.X)

        self.update_status()

    def create_ui(self):
        # Top control frame
        control_frame = tk.Frame(self.root, pady=4)
        control_frame.pack()

        # Color palette (20 solid colors)
        colors = [
            "#000000", "#808080", "#C0C0C0", "#FFFFFF", "#800000",
            "#FF0000", "#808000", "#FFFF00", "#008000", "#00FF00",
            "#008080", "#00FFFF", "#000080", "#0000FF", "#800080",
            "#FF00FF", "#A52A2A", "#FFA500", "#F5DEB3", "#DC143C"
        ]

        for c in colors:
            btn = tk.Button(control_frame, bg=c, width=2, command=lambda col=c: self.set_color(col))
            btn.pack(side=tk.LEFT, padx=1)

        # Pencil width slider
        self.slider = tk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL, label="Pen Width")
        self.slider.set(self.pen_width)
        self.slider.pack(side=tk.LEFT, padx=10)

        # Clear button
        clear_btn = tk.Button(control_frame, text="🧽 Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Save button
        save_btn = tk.Button(control_frame, text="💾 Save", command=self.save_drawing)
        save_btn.pack(side=tk.LEFT, padx=5)

    def set_color(self, new_color):
        self.pen_color = new_color
        self.update_status()

    def draw(self, event):
        self.pen_width = self.slider.get()

        if self.old_x and self.old_y:
            self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.pen_width, fill=self.pen_color,
                capstyle=tk.ROUND, smooth=True
            )

            # Calculate distance and time delta
            dist = math.sqrt((event.x - self.old_x)**2 + (event.y - self.old_y)**2)
            time_now = time.time()
            if self.last_time:
                dt = time_now - self.last_time
                if dt > 0:
                    self.speed = dist / dt
            self.last_time = time_now

        self.old_x = event.x
        self.old_y = event.y
        self.update_status()

    def reset(self, event):
        self.old_x = None
        self.old_y = None
        self.last_time = None
        self.speed = 0
        self.update_status()

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_drawing(self):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        img = ImageGrab.grab().crop((x, y, x1, y1))
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png")])
        if file_path:
            img.save(file_path)

    def update_status(self):
        status_text = f"🎨 Color: {self.pen_color}    ✏️ Width: {self.pen_width}    🏃 Speed: {self.speed:.2f} px/sec"
        self.status.config(text=status_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
