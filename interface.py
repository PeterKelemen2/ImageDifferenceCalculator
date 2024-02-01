# import tkinter
from tkinter import Tk, Label, LabelFrame, Button, StringVar, filedialog
from datetime import datetime

import debug

# Global properties
BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"
TIME_FONT_SIZE = 10
TIME_WRAPPER_WIDTH = 150
TIME_WRAPPER_HEIGHT = 100
WIN_WIDTH = 800
WIN_HEIGHT = 500


class Interface:
    def __init__(self):
        self.selected_file_path = None
        self.win = None
        self.time_label = None
        self.time_wrapper = None

        debug.log("[1/1] Creating interface...")

        self.set_properties()
        self.create_time_frame()
        self.create_browser()

        debug.log("[1/2] Interface created")
        self.win.mainloop()

    def set_properties(self):
        # Set windows properties
        debug.log("[2/1] Setting properties...")

        self.win = Tk()
        self.win["bg"] = BGCOLOR
        self.win.title("Image Difference Calculator")
        self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")
        self.selected_file_path = StringVar()

        debug.log("[2/2] Properties set!")

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)

    def create_time_frame(self):
        # Wrapper for time Label
        debug.log("[3/1] Creating Time Frame wrapper...")

        self.time_wrapper = LabelFrame(self.win,
                                       text="Time",
                                       width=TIME_WRAPPER_WIDTH,
                                       height=TIME_WRAPPER_HEIGHT)
        self.time_wrapper["bg"] = BGCOLOR
        self.time_wrapper.place(x=10, y=5)

        debug.log("[3/2] Time wrapper created!")

        # Label that shows the current time and date
        debug.log("[3/3] Creating Time Label...")

        self.time_label = Label(self.time_wrapper, text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        self.time_label.config(font=("Helvetica", TIME_FONT_SIZE),  # Font size
                               fg=BLACK,  # Font color
                               bg=BGCOLOR)  # Background color

        debug.log("[3/4] Time Label created!")

        # Set Frame label to width and height of Label
        debug.log("[3/5] Updating Time Label config...")
        label_width = self.time_label.winfo_reqwidth() + 20
        label_height = self.time_label.winfo_reqheight() * 2
        self.time_wrapper.config(font=("Helvetica", TIME_FONT_SIZE, "bold"),
                                 width=label_width,
                                 height=label_height)
        debug.log("[3/6] Time Label config updated!")

        # Pack Label in Frame
        debug.log("[3/7] Packing Time Label in Frame...")
        self.time_label.pack(padx=10,
                             pady=5,
                             anchor="center")
        debug.log("[3/8] Time Label packed!")
        # Schedule the update_label method to be called
        self.win.after(1000, self.update_label)

    def create_browser(self):
        # Wrapper for file browsing
        debug.log("[4/1] Creating Browsing wrapper...")
        button_wrapper = LabelFrame(self.win,
                                    text="Input file",
                                    bg=BGCOLOR,
                                    width=620,
                                    height=80,
                                    font=("Helvetica", TIME_FONT_SIZE, "bold"))
        # Place to the right
        x_coordinate = WIN_WIDTH - button_wrapper.winfo_reqwidth() - 10
        button_wrapper.place(x=x_coordinate, y=5)
        debug.log("[4/2] Browsing wrapper created!")

        # Button to initiate browsing
        debug.log("[4/3] Creating browse Button...")
        browse_button = (Button(button_wrapper,
                                text="Browse",
                                command=self.browse_files))
        # TODO: Figure out a way to make this not hardcoded
        browse_button.place(x=10,
                            y=10,
                            height=30,
                            width=70)
        debug.log("[4/4] Browse Button created!")

        # Label for showing opened file path
        debug.log("[4/5] Creating file path Label...")
        opened_file_label = Label(button_wrapper,
                                  textvariable=self.selected_file_path,
                                  bg=BGCOLOR,
                                  font=("Helvetica", TIME_FONT_SIZE))
        # Place right to the button, vertically centered
        opened_file_label.place(x=browse_button.winfo_reqwidth() * 2 - 12,
                                y=browse_button.winfo_reqheight() / 2)
        debug.log("[4/6] File path Label created!")

    def browse_files(self):
        # Open a file dialog and get the selected file path
        debug.log("Opening file browser dialog...")
        file_path = filedialog.askopenfilename(title="Select a file",
                                               filetypes=[("Text Files", "*.txt"),
                                                          ("Image Files", "*.jpg;*.png; *.jpeg;*.bmp"),
                                                          ("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv"),
                                                          ("All Files", "*.*")])

        # Update the label with the selected file path
        self.selected_file_path.set(file_path)
        debug.log(f"Selected file: {file_path}")
        if file_path:
            self.show_file_content(file_path)
        else:
            debug.log("No file selected")

    def show_file_content(self, path):
        # Wrapper for input file content
        debug.log("[5/1] Creating File content wrapper...")
        file_content_wrapper = LabelFrame(self.win,
                                          text="File content",
                                          bg=BGCOLOR,
                                          height=300,
                                          width=700)
        file_content_wrapper.pack(pady=150)
        debug.log("[5/2]File content wrapper created!")

        # File content
        debug.log("[5/3] Creating File content Label...")
        file_content_label = Label(file_content_wrapper,
                                   bg=BGCOLOR)
        file_content_label.pack()
        debug.log("[5/4]File content Label created!")

        # Reading file content
        debug.log("[5/5] Opening file...")
        output = ""
        # C:/Users/Administrator/PycharmProjects/ImageDifferenceCalculator/teszt.txt
        with open(path, "r") as file:
            for line in file:
                output += line
        debug.log("[5/6] File read, closed!")

        # Updating Label with the content
        debug.log("[5/7] Updating file content Label...")
        file_content_label.config(text=output)
        debug.log("[5/8] File content Label updated!")
