import tkinter
from datetime import datetime

import debug

BGCOLOR = "#00b685"
WHITE = "#ffffff"


class Interface:
    def __init__(self):
        debug.log("Creating interface...")
        self.win = tkinter.Tk()
        self.win["bg"] = BGCOLOR
        self.win.title("Image Difference Calculator")
        self.win.geometry("500x500")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")

        self.time_label = tkinter.Label(self.win, text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        self.time_label.config(font=("Helvetica", 25), fg=WHITE, bg=BGCOLOR)

        self.time_label.place(x=250, y=250, anchor="center")

        self.win.after(1000, self.update_label)

        debug.log("Interface created")
        self.win.mainloop()

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)
