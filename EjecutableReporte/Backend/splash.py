import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import time
import os

class SplashScreen:
    def __init__(self, gif_path, duration=3):
        self.width = 420
        self.height = 420
        self.duration = duration

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#2b2436")

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="#2b2436",
            highlightthickness=0
        )
        self.canvas.pack()

        # Fondo degradado pastel
        self.draw_gradient("#f6d6e8", "#c7b6e8")  

        # Marco redondeado (fake)
        self.canvas.create_rectangle(
            10, 10, self.width - 10, self.height - 10,
            outline="#ffffff", width=2
        )
        
        #Cargar GIF
        self.frames = []
        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.resize((260, 260), Image.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(frame))
        
        self.image_id = self.canvas.create_image(
            self.width // 2,
            self.height // 2 - 20,
            image=self.frames[0]
        )
        
        self.loading_text = "Cargando interfaz"
        self.dot_count = 0
        
        #Texto cute
        self.text_id = self.canvas.create_text(
            self.width // 2,
            self.height - 60,
            text=self.loading_text,
            fill="#ffffff",
            font=("Segoe UI", 12, "bold")
        )
        
        self.animate_text()
        self.center_window()
        self.animate(0)
        
        threading.Thread(target=self.close_after_delay, daemon=True).start()
        self.root.mainloop()
        
    def draw_gradient(self, color1, color2):
        r1, g1, b1 = self.root.winfo_rgb(color1)
        r2, g2, b2 = self.root.winfo_rgb(color2)
        
        r_ratio = (r2 - r1) / self.height
        g_ratio = (g2 - g1) / self.height
        b_ratio = (b2 - b1) / self.height
        
        for i in range(self.height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr>>8:02x}{ng>>8:02x}{nb>>8:02x}"
            self.canvas.create_line(0, i, self.width, i, fill=color)
    
    def center_window(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - self.width) // 2
        y = (screen_h - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
    def animate(self, index):
        self.canvas.itemconfig(self.image_id,image=self.frames[index])
        self.root.after(90, self.animate, (index + 1) % len(self.frames))
        
    def animate_text(self):
        dots = "." * self.dot_count
        self.canvas.itemconfig(
            self.text_id,
            text=f"{self.loading_text}{dots}"
        )
        
        self.dot_count = (self.dot_count + 1) % 4
        self.root.after(500, self.animate_text)
        
    def close_after_delay(self):
        time.sleep(self.duration)
        self.root.destroy()


def show_splash():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(base_dir, "assets", "splash.gif")
    SplashScreen(gif_path)
