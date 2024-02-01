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
        debug.log("Creating interface...")
        # Set windows properties
        self.win = tkinter.Tk()
        self.win["bg"] = BGCOLOR
        self.win.title("Image Difference Calculator")
        self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")

        # Wrapper for time Label
        self.time_frame = tkinter.LabelFrame(self.win, text="Time", width=150, height=100)
        self.time_frame["bg"] = BGCOLOR
        self.time_frame.place(x=10, y=5)

        # Label that shows the current time and date
        self.time_label = tkinter.Label(self.time_frame, text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        self.time_label.config(font=("Helvetica", TIME_FONT_SIZE),  # Font size
                               fg=BLACK,  # Font color
                               bg=BGCOLOR)  # Background color

        # Set Frame label to width and height of Label
        label_width = self.time_label.winfo_reqwidth() + 20
        label_height = self.time_label.winfo_reqheight() * 2
        self.time_frame.config(font=("Helvetica", TIME_FONT_SIZE, "bold"),
                               width=label_width,
                               height=label_height)

        # Pack Label in Frame
        self.time_label.pack(padx=10, pady=5, anchor="center")
        # Schedule the update_label method to be called
        self.win.after(1000, self.update_label)

        debug.log("Interface created")
        self.win.mainloop()

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)
