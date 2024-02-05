BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"

from tkinter import Canvas, Tk, BOTH


class RoundedRectangleButton:
    def __init__(self, master, text, command=None, width=100, height=40, radius=10, bg="white", fg="black",
                 font=("Helvetica", 10, "bold")):
        self.master = master
        self.command = command

        self.canvas = Canvas(master, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack()

        self.create_rounded_rectangle(width, height, radius, bg)
        self.canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=font)

        self.canvas.bind("<Button-1>", self.on_button_click)

    def create_rounded_rectangle(self, width, height, radius, color):
        x0, y0 = 0, 0
        x1, y1 = width, height
        self.canvas.create_arc(x0, y0, x0 + 2 * radius, y0 + 2 * radius, start=90, extent=90, outline=color,
                               fill=color, width=0)
        self.canvas.create_arc(x1 - 2 * radius, y0, x1, y0 + 2 * radius, start=0, extent=90, outline=color, fill=color,
                               width=0)
        self.canvas.create_arc(x0, y1 - 2 * radius, x0 + 2 * radius, y1, start=180, extent=90, outline=color,
                               fill=color, width=0)
        self.canvas.create_arc(x1 - 2 * radius, y1 - 2 * radius, x1, y1, start=270, extent=90, outline=color,
                               fill=color,
                               width=0)
        self.canvas.create_rectangle(x0 + radius, y0, x1 - radius, y1, outline=color, fill=color, width=0)
        self.canvas.create_rectangle(x0, y0 + radius, x1, y1 - radius, outline=color, fill=color, width=0)

    def on_button_click(self, event):
        if self.command:
            self.command()

    def winfo_reqwidth(self):
        return self.canvas.winfo_reqwidth()

    def winfo_reqheight(self):
        return self.canvas.winfo_reqheight()
