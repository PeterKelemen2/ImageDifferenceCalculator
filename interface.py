# import tkinter
from tkinter import Tk, Label, LabelFrame, Button, StringVar, filedialog, PhotoImage, Canvas, Frame

import cv2
from PIL import Image, ImageTk
from datetime import datetime

import debug

import custom_button
from media_player import MediaPlayer

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
                                       height=TIME_WRAPPER_HEIGHT,
                                       bg=BGCOLOR)

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

        browse_button = custom_button.RoundedRectangleButton(button_wrapper,
                                                             text="Browse",
                                                             command=self.browse_files,
                                                             width=70,
                                                             height=30)
        browse_button.canvas.place(x=10, y=10)

        debug.log("[4/4] Browse Button created!")

        # Label for showing opened file path
        debug.log("[4/5] Creating file path Label...")
        opened_file_label = Label(button_wrapper,
                                  textvariable=self.selected_file_path,
                                  bg=BGCOLOR,
                                  font=("Helvetica", TIME_FONT_SIZE),
                                  wraplength=520,
                                  justify="left")
        # Place right to the button, vertically centered
        opened_file_label.place(x=browse_button.winfo_reqwidth() * 2 - 55,
                                y=browse_button.winfo_reqheight() / 2 - 5)
        debug.log("[4/6] File path Label created!")

    def browse_files(self):
        # Open a file dialog and get the selected file path
        debug.log("Opening file browser dialog...")
        file_path = filedialog.askopenfilename(title="Select a file",
                                               filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv"),
                                                          ("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),
                                                          ("Text Files", "*.txt"),
                                                          ("All Files", "*.*")])

        # Update the label with the selected file path
        self.selected_file_path.set(file_path)
        debug.log(f"Selected file: {file_path}")
        if file_path:
            self.show_first_frame_details(file_path)
        else:
            debug.log("No file selected")

    def show_first_frame_details(self, path: str):
        """
        Display video details, including the first frame, in a labeled frame.

        Parameters:
        - path (str): The path to the video file.

        This method creates a labeled frame containing the first frame of the video and details about the video.
        The video details include the width, height, framerate, and bitrate.
        """

        # Creating a labeled frame to contain video details
        debug.log("[5/1] Creating video details wrapper...")
        frame_wrapper = LabelFrame(self.win,
                                   text="Video Data",
                                   bg=BGCOLOR,
                                   width=780,
                                   height=320,
                                   font=("Helvetica", 10, "bold"))
        frame_wrapper.place(x=10, y=100)
        debug.log("[5/2] Video details wrapper created!")

        # Creating a label to display the first frame of the video
        debug.log("[5/3] Creating placeholder label for first frame...")
        frame_label = Label(frame_wrapper)
        frame_label.place(x=5, y=5)
        debug.log("[5/4] First frame placeholder created!")

        # Opening the video and extracting details from the first frame
        debug.log("[5/5] Opening video file and getting first frame data")
        cap = cv2.VideoCapture(path)
        fps = "{:.2f}".format(cap.get(cv2.CAP_PROP_FPS))
        bitrate = "{:.0f}".format(cap.get(cv2.CAP_PROP_BITRATE))
        ret, frame = cap.read()
        cap.release()
        debug.log("[5/6] First frame data gathered!")

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)

            # Extracting video details from the first frame
            width, height = image.size
            aspect_ratio = width / height
            im_det = (f"Width: {image.width}px\n"
                      f"Height: {image.height}px\n"
                      f"Framerate: {fps} fps\n"
                      f"Bitrate: {bitrate} kbps")

            # Resizing the first frame to fit within the frame wrapper
            debug.log("[5/7] Calculating first frame information...")
            new_width = frame_wrapper.winfo_reqwidth() // 2
            new_height = int(new_width / aspect_ratio)
            image = image.resize((new_width, new_height), Image.BILINEAR)
            image_file = ImageTk.PhotoImage(image)
            debug.log("[5/8] First image information set!")

            # Configuring the frame label with the resized first frame
            debug.log("[5/9] Configuring image...")
            frame_label.config(image=image_file)
            frame_label.image = image_file
            debug.log("[5/10] Image configured!")

        # media_player_button = Button(frame_wrapper, text="Open Media Player")
        media_player_button = custom_button.RoundedRectangleButton(frame_wrapper,
                                                                   text="Open Media Player",
                                                                   width=140)
        media_player_button.canvas.place(x=10,
                                         y=new_height + 15)

        # Creating labels to display video details
        debug.log("[5/11] Creating labels to display video details...")
        frame_details_header = Label(frame_wrapper,
                                     text="Video details:",
                                     bg=BGCOLOR,
                                     font=("Helvetica", 10, "bold")
                                     )
        frame_details_header.place(x=new_width + 30, y=10)
        image_details = Label(frame_wrapper,
                              text=im_det,
                              bg=BGCOLOR,
                              font=("Helvetica", 10),
                              # Left alignment
                              justify="left",
                              anchor="w"
                              )
        image_details.place(x=new_width + 30, y=frame_details_header.winfo_reqheight() * 1.5)
        debug.log("[5/12] Labels to display video details created!")

    def open_media_player(self, file_path):
        video_window = Tk()
        app = MediaPlayer(video_window, file_path)
        video_window.mainloop()
