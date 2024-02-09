from tkinter import Tk, Canvas, PhotoImage
from PIL import Image, ImageDraw

BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"

wide_button = "assets/wide_button.png"
wide_button_clicked = "assets/wide_button_clicked.png"
button = "assets/button.png"
button_clicked = "assets/button_clicked.png"


class CustomButton:
    def __init__(self, master, text, command=None, width=110, height=30, fg="black",
                 font=("Helvetica", 10, "bold"), type=wide_button):
        self.master = master
        self.command = command

        # Store the PhotoImage objects as attributes to prevent garbage collection
        self.button_image = None
        self.button_image_clicked = None

        if type == wide_button:
            self.button_image = PhotoImage(file=wide_button)
            self.button_image_clicked = PhotoImage(file=wide_button_clicked)
        elif type == button:
            self.button_image = PhotoImage(file=button)
            self.button_image_clicked = PhotoImage(file=button_clicked)
            width = 70

        self.canvas = Canvas(master, width=width, height=height, highlightthickness=0)
        self.canvas.pack()

        if self.button_image:
            self.image_item = self.canvas.create_image(width // 2, height // 2, anchor="center",
                                                       image=self.button_image)

        # Create text on top of the background
        self.text_item = self.canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=font)

        # Bind click event
        self.canvas.tag_bind(self.text_item, "<Button-1>", self.on_button_click)

    def on_button_click(self, event):
        if self.command:
            self.command()

        if self.button_image_clicked:
            self.canvas.itemconfig(self.image_item, image=self.button_image_clicked)
            self.canvas.update()
            self.master.after(50, self.switch_back_to_regular)

    def switch_back_to_regular(self):
        if self.button_image:
            self.canvas.itemconfig(self.image_item, image=self.button_image)

    def winfo_reqwidth(self):
        return self.canvas.winfo_reqwidth()

    def winfo_reqheight(self):
        return self.canvas.winfo_reqheight()
