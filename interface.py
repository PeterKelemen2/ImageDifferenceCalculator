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
        self.create_buttons()

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

    def create_buttons(self):
        button_wrapper = LabelFrame(self.win,
                                    text="Input file",
                                    bg=BGCOLOR,
                                    width=620,
                                    height=80,
                                    font=("Helvetica", TIME_FONT_SIZE, "bold"))
        # Place to the right
        x_coordinate = WIN_WIDTH - button_wrapper.winfo_reqwidth() - 10
        button_wrapper.place(x=x_coordinate, y=5)

        browse_button = (Button(button_wrapper,
                                text="Browse",
                                command=self.browse_files))
        browse_button.place(x=10,
                            y=10,
                            height=30,
                            width=70)

        opened_file_label = Label(button_wrapper,
                                  textvariable=self.selected_file_path,
                                  bg=BGCOLOR,
                                  font=("Helvetica", TIME_FONT_SIZE))
        opened_file_label.place(x=browse_button.winfo_reqwidth() * 2 - 12,
                                y=browse_button.winfo_reqheight() / 2)

    def browse_files(self):
        # Open a file dialog and get the selected file path
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All Files", "*.*")])

        # Update the label with the selected file path
        self.selected_file_path.set(file_path)
        debug.log(f"Selected file: {file_path}")
