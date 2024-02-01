import tkinter
from datetime import datetime

import debug

# Global properties
BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"
TIME_FONT_SIZE = 10
WIN_WIDTH = 500
WIN_HEIGHT = 500


class Interface:
    def __init__(self):
        self.win = None
        self.time_label = None
        self.time_wrapper = None

        debug.log("Creating interface... [1/1]")

        self.set_properties()
        self.create_time_frame()

        debug.log("Interface created [1/2]")
        self.win.mainloop()

    def set_properties(self):
        # Set windows properties
        debug.log("Setting properties... [2/1]")
        self.win = tkinter.Tk()
        self.win["bg"] = BGCOLOR
        self.win.title("Image Difference Calculator")
        self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")
        debug.log("Properties set! [2/2]")

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)

    def create_time_frame(self):
        # Wrapper for time Label
        debug.log("Creating Time Frame wrapper... [3/1]")
        self.time_wrapper = tkinter.LabelFrame(self.win, text="Time", width=150, height=100)
        self.time_wrapper["bg"] = BGCOLOR
        self.time_wrapper.place(x=10, y=5)
        debug.log("Time wrapper created! [3/2]")

        # Label that shows the current time and date
        debug.log("Creating Time Label... [3/3]")
        self.time_label = tkinter.Label(self.time_wrapper, text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        self.time_label.config(font=("Helvetica", TIME_FONT_SIZE),  # Font size
                               fg=BLACK,  # Font color
                               bg=BGCOLOR)  # Background color
        debug.log("Time Label created! [3/4]")

        # Set Frame label to width and height of Label
        debug.log("Updating Time Label config... [3/5]")
        label_width = self.time_label.winfo_reqwidth() + 20
        label_height = self.time_label.winfo_reqheight() * 2
        self.time_wrapper.config(font=("Helvetica", TIME_FONT_SIZE, "bold"),
                                 width=label_width,
                                 height=label_height)
        debug.log("Time Label config updated! [3/6]")

        # Pack Label in Frame
        debug.log("Packing Time Label in Frame... [3/7]")
        self.time_label.pack(padx=10, pady=5, anchor="center")
        debug.log("Time Label packed! [3/8]")
        # Schedule the update_label method to be called
        self.win.after(1000, self.update_label)
