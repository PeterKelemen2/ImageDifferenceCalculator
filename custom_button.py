from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageDraw

BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"


class RoundedRectangleButton:
    def __init__(self, master, text, command=None, width=100, height=40, radius=10, bg="white", fg="black",
                 font=("Helvetica", 10, "bold")):
        self.master = master
        self.command = command

        self.canvas = Canvas(master, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack()

        rounded_button_image = self.create_rounded_button_image(width, height, radius, bg)
        self.photo_image = PhotoImage(width=width, height=height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image, state="normal")
        self.canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=font)

        self.canvas.bind("<Button-1>", self.on_button_click)

    def create_rounded_button_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rectangle([radius, 0, width - radius, height], fill=color)
        draw.rectangle([0, radius, width, height - radius], fill=color)
        draw.pieslice([0, 0, radius * 2, radius * 2], 90, 180, fill=color)
        draw.pieslice([width - radius * 2, 0, width, radius * 2], 0, 90, fill=color)
        draw.pieslice([0, height - radius * 2, radius * 2, height], 180, 270, fill=color)
        draw.pieslice([width - radius * 2, height - radius * 2, width, height], 270, 360, fill=color)

        return image.tobytes("raw", "RGBA")

    def on_button_click(self, event):
        if self.command:
            self.command()

    def winfo_reqwidth(self):
        return self.canvas.winfo_reqwidth()

    def winfo_reqheight(self):
        return self.canvas.winfo_reqheight()
