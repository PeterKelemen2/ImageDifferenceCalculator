from tkinter import PhotoImage, Canvas

import PIL.ImageOps
from PIL import Image, ImageTk

import custom_button
import interface

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
    def __init__(self, master, width, height, text=None, fill=BLACK, fg=WHITE, bg=BGCOLOR, radius=10):
        self.width = width
        self.height = height
        self.fill = fill
        self.fg = interface.FONT_COLOR
        self.bg = bg
        self.text = text
        self.radius = radius
        self.canvas = Canvas(master, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack()

        self.item_list = list()
        self.rect_im = None
        self.circle_im = None
        self.rect_im_hor = None
        self.overlay = None
        self.rect_im_ver = None
        self.rect_im_center = None
        self.text_item = None
        self.cir1 = None
        self.cir2 = None
        self.cir3 = None
        self.cir4 = None
        self.rec1 = None
        self.rec2 = None
        self.rec3 = None
        self.rec4 = None
        self.center = None
        self.cir_im = None
        self.rec_im_hor = None
        self.rec_im_ver = None
        self.center_rec = None

        self.create_images()
        self.create_labelframe()

    def load_images(self):
        # Load the images using PIL
        self.circle_im = None
        self.rect_im = None
        self.circle_im = Image.open(circle).convert("RGBA")
        self.rect_im = Image.open(rect).convert("RGBA")

    def create_images(self):
        # Overlay fill color on images

        self.load_images()

        self.overlay = Image.new("RGBA", self.circle_im.size, self.fill)
        self.circle_im = Image.composite(self.overlay, self.circle_im, self.circle_im)
        self.rect_im = Image.composite(self.overlay, self.rect_im, self.rect_im)

        # Resize the image (width, height)
        self.circle_im = self.circle_im.resize((self.radius * 2, self.radius * 2))
        self.rect_im_hor = self.rect_im.resize((self.width - self.radius * 2, self.radius * 2))
        self.rect_im_ver = self.rect_im.resize((self.radius * 2, self.height - self.radius * 2))
        self.rect_im_center = self.rect_im.resize((self.width - 2 * self.radius, self.height - 2 * self.radius))

    def create_labelframe(self):
        self.item_list = list()
        self.cir_im = ImageTk.PhotoImage(self.circle_im)
        self.rec_im_hor = ImageTk.PhotoImage(self.rect_im_hor)
        self.rec_im_ver = ImageTk.PhotoImage(self.rect_im_ver)
        self.center_rec = ImageTk.PhotoImage(self.rect_im_center)

        # Create circles (x,y)
        self.item_list.append(self.canvas.create_image(self.radius, self.radius, anchor="center", image=self.cir_im))
        self.item_list.append(
            self.canvas.create_image(self.width - self.radius, self.radius, anchor="center", image=self.cir_im))
        self.item_list.append(
            self.canvas.create_image(self.radius, self.height - self.radius, anchor="center", image=self.cir_im))
        self.item_list.append(
            self.canvas.create_image(self.width - self.radius, self.height - self.radius, anchor="center",
                                     image=self.cir_im))
        # self.item_list.append(self.cir1, self.cir2, self.cir3, self.cir4)

        self.item_list.append(self.canvas.create_image(self.radius, self.radius, anchor="w", image=self.rec_im_hor))
        self.item_list.append(
            self.canvas.create_image(self.radius, self.height - self.radius, anchor="w", image=self.rec_im_hor))
        self.item_list.append(
            self.canvas.create_image(self.radius, self.height - self.radius, anchor="s", image=self.rec_im_ver))
        self.item_list.append(self.canvas.create_image(self.width - self.radius, self.height - self.radius, anchor="s",
                                                       image=self.rec_im_ver))

        self.item_list.append(self.canvas.create_image(self.radius, self.radius, anchor="nw", image=self.center_rec))

        self.text_item = self.canvas.create_text(self.radius, self.radius, text=self.text, fill=self.fg, anchor="w",
                                                 font=BOLD_FONT)

    def config(self, text=None, fg=None, bg=None, fill=None):
        if text is not None:
            self.text = text
            self.canvas.itemconfig(self.text_item, text=self.text)
        if fg is not None:
            self.fg = fg
            self.canvas.itemconfig(self.text_item, fill=self.fg)
        if bg is not None:
            self.bg = bg
            self.canvas.config(bg=self.bg)
        if fill is not None:
            self.change_fill_color(fill)

    def switch_theme(self, new_fill=None, new_text_color=None, new_bg=None, buttons=None, labels=None):
        if new_fill is not None: self.change_fill_color(new_fill)
        if new_text_color is not None: self.change_text_color(new_text_color)
        if new_bg is not None: self.canvas.config(bg=new_bg)
        if self.canvas.winfo_children():
            for child in self.canvas.winfo_children():
                if "text" in child.keys():
                    child.config(fg=new_text_color)
        if buttons is not None:
            for button in buttons:
                if button is not None:
                    button.config(bg=new_fill)
        if labels is not None:
            for label in labels:
                if label is not None:
                    label.config(bg=new_fill, fg=new_text_color)

    def change_fill_color(self, new_color):
        self.fill = new_color
        self.create_images()
        self.create_labelframe()

    def change_text_color(self, new_color):
        self.fg = new_color
        self.canvas.itemconfig(self.text_item, fill=self.fg)

    def get_label_width(self):
        bbox = self.canvas.bbox(self.text_item)
        width = bbox[2] - bbox[0]
        return width

    def set_label_text(self, new_text):
        if self.canvas is not None:
            self.canvas.itemconfig(self.text_item, text=new_text)

    def get_label_height(self):
        bbox = self.canvas.bbox(self.text_item)
        height = bbox[3] - bbox[1]
        return height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
