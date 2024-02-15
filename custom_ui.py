from tkinter import PhotoImage, Canvas

from PIL import Image, ImageTk

bg_path = "assets/rounded_frame.png"
circle = "assets/circle.png"
rect = "assets/black.png"

BGCOLOR = "#3a3a3a"
DARKER_BG = "#292929"
WHITE = "#ffffff"
BLACK = "#000000"

FONT_COLOR = "#ffffff"
TIME_FONT_SIZE = 12
BIG_FONT_SIZE = 14
FONT = ("Ubuntu", TIME_FONT_SIZE)
BOLD_FONT = ("Ubuntu", TIME_FONT_SIZE, "bold")
BIG_FONT = ("Ubuntu", BIG_FONT_SIZE)
BIG_FONT_BOLD = ("Ubuntu", BIG_FONT_SIZE, "bold")


class CustomLabelFrame:
    def __init__(self, master, width, height, text="", fg=WHITE, bg=BGCOLOR):
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.text = text
        self.canvas = Canvas(master, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack()

        self.cir = None
        self.rec = None

        # Load the images using PIL
        circle_im = Image.open(circle)
        rect_im = Image.open(rect)

        # Resize the image
        circle_im = circle_im.resize((30, 30))
        rect_im = rect_im.resize((width - circle_im.size[0] // 2, circle_im.size[0]))

        # Convert the resized image to a Tkinter PhotoImage object
        self.cir_im = ImageTk.PhotoImage(circle_im)
        self.rec_im = ImageTk.PhotoImage(rect_im)

        # Display the resized image on the canvas
        self.cir = self.canvas.create_image(15, 30, anchor="center", image=self.cir_im)
        self.rec = self.canvas.create_image(15, 30, anchor="w", image=self.rec_im)
        # self.text_item = self.canvas.create_text(10, 15, text=text, fill=fg, anchor="w", font=FONT)
