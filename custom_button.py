from tkinter import Canvas, PhotoImage

# BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"
TRANSPARENT = "#00000000"

wide_button = "assets/wide_button2.png"
wide_button_clicked = "assets/wide_button2_clicked.png"
button = "assets/button2.png"
button_clicked = "assets/button2_clicked.png"
settings_button = "assets/cog_button.png"
settings_button_clicked = "assets/cog_button_clicked.png"


class CustomButton:
    def __init__(self, master, text="", command=None, width=110, height=30, fg="black", bg=WHITE,
                 font=("Helvetica", 10, "bold"), button_type=wide_button):
        self.master = master
        self.command = command
        self.button_state = "enabled"

        # Store the PhotoImage objects as attributes to prevent garbage collection
        self.button_image = None
        self.button_image_clicked = None
        self.image_item = None

        if button_type == wide_button:
            self.button_image = PhotoImage(file=wide_button)
            self.button_image_clicked = PhotoImage(file=wide_button_clicked)
        elif button_type == button:
            width = 70
            self.button_image = PhotoImage(file=button)
            self.button_image_clicked = PhotoImage(file=button_clicked)
        elif button_type == settings_button:
            width = 60
            height = 60
            self.button_image = PhotoImage(file=settings_button)
            self.button_image_clicked = PhotoImage(file=settings_button_clicked)
            # self.button_image_clicked = self.button_image_clicked.subsample(2)

        self.canvas = Canvas(master, width=width, height=height, highlightthickness=0, bg=bg)
        self.canvas.pack()
        # self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        if self.button_image:
            self.image_item = self.canvas.create_image(width // 2, height // 2, anchor="center",
                                                       image=self.button_image)

        # Create text on top of the background
        self.text_item = self.canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=font)

        # Bind click event
        if self.image_item:
            self.canvas.tag_bind(self.image_item, "<Button-1>", self.on_button_click)
            self.canvas.tag_bind(self.text_item, "<Button-1>", self.on_button_click)
        else:
            self.canvas.tag_bind(self.text_item, "<Button-1>", self.on_button_click)

    def on_button_click(self, event):
        if self.command and self.button_state == "enabled":
            self.command()

        if self.button_image_clicked:
            self.canvas.itemconfig(self.image_item, image=self.button_image_clicked)
            self.canvas.update()
            self.master.after(50, self.switch_back_to_regular)

    def enable(self):
        self.button_state = "enabled"

    def disable(self):
        self.button_state = "disabled"

    def is_enabled(self):
        if self.button_state == "enabled":
            return True
        return False

    def switch_back_to_regular(self):
        if self.button_image:
            self.canvas.itemconfig(self.image_item, image=self.button_image)

    def winfo_reqwidth(self):
        return self.canvas.winfo_reqwidth()

    def winfo_reqheight(self):
        return self.canvas.winfo_reqheight()
