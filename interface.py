import tkinter
import debug

BGCOLOR = "#00b685"


class Interface:
    def __init__(self):
        debug.log("Creating interface...")
        self.root = tkinter.Tk()
        self.root["bg"] = BGCOLOR
        self.root.title("Image Difference Calculator")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW")
        debug.log("Interface created")
        self.root.mainloop()
