from tkinter import PhotoImage, Canvas

import PIL.ImageOps
from PIL import Image, ImageTk

bg_path = "assets/rounded_frame.png"
circle = "assets/frame_circle.png"
rect = "assets/frame_square.png"

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
    def __init__(self, master, width, height, text="", fill=BLACK, fg=WHITE, bg=BGCOLOR, radius=10):
        self.width = width
        self.height = height
        self.fill = fill
        self.fg = fg
        self.bg = bg
        self.text = text
        self.radius = radius
        self.canvas = Canvas(master, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack()

        # self.cir1 = None
        # self.cir2 = None
        # self.cir3 = None
        # self.cir4 = None
        # self.rec1 = None
        # self.rec2 = None
        # self.rec3 = None
        # self.rec4 = None
        # self.center = None
        # self.cir_im = None
        # self.rec_im_hor = None
        # self.rec_im_ver = None
        # self.center_rec = None

        # Load the images using PIL
        circle_im = Image.open(circle).convert("RGBA")
        rect_im = Image.open(rect).convert("RGBA")

        # Overlay fill color on images
        overlay = Image.new("RGBA", circle_im.size, fill)
        circle_im = Image.composite(overlay, circle_im, circle_im)
        rect_im = Image.composite(overlay, rect_im, rect_im)

        # Resize the image (width, height)
        circle_im = circle_im.resize((radius * 2, radius * 2))
        rect_im_hor = rect_im.resize((width - radius * 2, radius * 2))
        rect_im_ver = rect_im.resize((radius * 2, height - radius * 2))
        rect_im_center = rect_im.resize((width - 2 * radius, height - 2 * radius))

        # Convert the resized image to a Tkinter PhotoImage object
        self.cir_im = ImageTk.PhotoImage(circle_im)
        self.rec_im_hor = ImageTk.PhotoImage(rect_im_hor)
        self.rec_im_ver = ImageTk.PhotoImage(rect_im_ver)
        self.center_rec = ImageTk.PhotoImage(rect_im_center)

        # Create circles (x,y)
        self.cir1 = self.canvas.create_image(radius, radius, anchor="center", image=self.cir_im)
        self.cir2 = self.canvas.create_image(width - radius, radius, anchor="center", image=self.cir_im)
        self.cir3 = self.canvas.create_image(radius, height - radius, anchor="center", image=self.cir_im)
        self.cir4 = self.canvas.create_image(width - radius, height - radius, anchor="center", image=self.cir_im)

        self.rec1 = self.canvas.create_image(radius, radius, anchor="w", image=self.rec_im_hor)
        self.rec2 = self.canvas.create_image(radius, height - radius, anchor="w", image=self.rec_im_hor)
        self.rec3 = self.canvas.create_image(radius, height - radius, anchor="s", image=self.rec_im_ver)
        self.rec3 = self.canvas.create_image(width - radius, height - radius, anchor="s", image=self.rec_im_ver)

        self.center = self.canvas.create_image(radius, radius, anchor="nw", image=self.center_rec)

        self.text_item = self.canvas.create_text(radius, radius, text=text, fill=fg, anchor="w", font=BOLD_FONT)
