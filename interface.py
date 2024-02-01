import tkinter
from datetime import datetime

import debug

# Global properties
BGCOLOR = "#00b685"
WHITE = "#ffffff"
TIME_FONT_SIZE = 10
WIN_WIDTH = 500
WIN_HEIGHT = 500


class Interface:
    def __init__(self):
        debug.log("Creating interface...")
        # Set windows properties
        self.win = tkinter.Tk()
        self.win["bg"] = BGCOLOR
        self.win.title("Image Difference Calculator")
        self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")

        # Label that shows the current time and date
        self.time_label = tkinter.Label(self.win, text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        self.time_label.config(font=("Helvetica", TIME_FONT_SIZE),  # Font size
                               fg=WHITE,  # Font color
                               bg=BGCOLOR)  # Background color
        # Absolute position
        self.time_label.place(x=10, y=10)
        # Schedule the update_label method to be called
        self.win.after(1000, self.update_label)

        debug.log("Interface created")
        self.win.mainloop()

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)
