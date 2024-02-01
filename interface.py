import tkinter
from datetime import datetime

import debug

# Global properties
BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"
TIME_FONT_SIZE = 10
TIME_WRAPPER_WIDTH = 150
TIME_WRAPPER_HEIGHT = 100
WIN_WIDTH = 500
WIN_HEIGHT = 500


class Interface:
    def __init__(self):
        self.win = None
        self.time_label = None
        self.time_wrapper = None

        debug.log("[1/1] Creating interface...")

        self.set_properties()
        self.create_time_frame()

        debug.log("[1/2] Interface created")
        self.win.mainloop()

    def set_properties(self):
        # Set windows properties
        debug.log("[2/1] Setting properties...")

        self.win = tkinter.Tk()
        self.win["bg"] = BGCOLOR
        self.win.title("Image Difference Calculator")
        self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")

        debug.log("[2/2] Properties set!")

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)

    def create_time_frame(self):
        # Wrapper for time Label
        debug.log("[3/1] Creating Time Frame wrapper...")

        self.time_wrapper = tkinter.LabelFrame(self.win,
                                               text="Time",
                                               width=TIME_WRAPPER_WIDTH,
                                               height=TIME_WRAPPER_HEIGHT)
        self.time_wrapper["bg"] = BGCOLOR
        self.time_wrapper.place(x=10, y=5)

        debug.log("[3/2] Time wrapper created!")

        # Label that shows the current time and date
        debug.log("[3/3] Creating Time Label...")

        self.time_label = tkinter.Label(self.time_wrapper, text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
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
        self.time_label.pack(padx=10, pady=5, anchor="center")
        debug.log("[3/8] Time Label packed!")
        # Schedule the update_label method to be called
        self.win.after(1000, self.update_label)
