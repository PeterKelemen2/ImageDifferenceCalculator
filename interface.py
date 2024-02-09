import time
from tkinter import Tk, Label, LabelFrame, Button, StringVar, filedialog, PhotoImage
from tkinter.ttk import Progressbar

import cv2

from PIL import Image, ImageTk
from datetime import datetime

import debug

import custom_button
import processing
import vlc_handler

# Global properties
BGCOLOR = "#00b685"
WHITE = "#ffffff"
BLACK = "#000000"
TIME_FONT_SIZE = 10
TIME_WRAPPER_WIDTH = 150
TIME_WRAPPER_HEIGHT = 100
WIN_WIDTH = 800
WIN_HEIGHT = 500
call_nr = 0
video_file_path = None


class Interface:
    def __init__(self):
        self.selected_file_path = None
        self.win = None
        self.time_label = None
        self.time_wrapper = None
        self.progress_bar = None
        self.progress_label = None

        debug.log("[1/1] Creating interface...", text_color="blue")

        self.set_properties()
        self.create_time_frame()
        self.create_browser()

        debug.log("[1/2] Interface created", text_color="blue")
        self.win.mainloop()

    def set_properties(self):
        # Set windows properties
        debug.log("[2/1] Setting properties...", text_color="magenta")

        self.win = Tk()
        self.win["bg"] = BGCOLOR
        self.win.title("Image Difference Calculator")
        self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")
        self.selected_file_path = StringVar()

        debug.log("[2/2] Properties set!", text_color="magenta")

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)

    def create_time_frame(self):
        # Wrapper for time Label
        debug.log("[3/1] Creating Time Frame wrapper...", text_color="yellow")

        self.time_wrapper = LabelFrame(self.win,
                                       text="Time",
                                       width=TIME_WRAPPER_WIDTH,
                                       height=TIME_WRAPPER_HEIGHT,
                                       bg=BGCOLOR)

        self.time_wrapper.place(x=10, y=5)

        debug.log("[3/2] Time wrapper created!", text_color="yellow")

        # Label that shows the current time and date
        debug.log("[3/3] Creating Time Label...", text_color="yellow")

        self.time_label = Label(self.time_wrapper, text=datetime.now().strftime("%Y.%m.%d - %H:%M:%S"))
        self.time_label.config(font=("Helvetica", TIME_FONT_SIZE),  # Font size
                               fg=BLACK,  # Font color
                               bg=BGCOLOR)  # Background color

        debug.log("[3/4] Time Label created!", text_color="yellow")

        # Set Frame label to width and height of Label
        debug.log("[3/5] Updating Time Label config...", text_color="yellow")
        label_width = self.time_label.winfo_reqwidth() + 20
        label_height = self.time_label.winfo_reqheight() * 2
        self.time_wrapper.config(font=("Helvetica", TIME_FONT_SIZE, "bold"),
                                 width=label_width,
                                 height=label_height)
        debug.log("[3/6] Time Label config updated!", text_color="yellow")

        # Pack Label in Frame
        debug.log("[3/7] Packing Time Label in Frame...", text_color="yellow")
        self.time_label.pack(padx=10,
                             pady=5,
                             anchor="center")
        debug.log("[3/8] Time Label packed!", text_color="yellow")
        # Schedule the update_label method to be called
        self.win.after(1000, self.update_label)

    def create_browser(self):
        # Wrapper for file browsing
        debug.log("[4/1] Creating Browsing wrapper...", text_color="magenta")
        button_wrapper = LabelFrame(self.win,
                                    text="Input file",
                                    bg=BGCOLOR,
                                    width=620,
                                    height=80,
                                    font=("Helvetica", TIME_FONT_SIZE, "bold"))
        # Place to the right
        x_coordinate = WIN_WIDTH - button_wrapper.winfo_reqwidth() - 10
        button_wrapper.place(x=x_coordinate, y=5)
        debug.log("[4/2] Browsing wrapper created!", text_color="magenta")

        # Button to initiate browsing
        debug.log("[4/3] Creating browse Button...", text_color="magenta")

        browse_button = custom_button.RoundedRectangleButton(button_wrapper,
                                                             text="Browse",
                                                             command=self.browse_files,
                                                             width=70,
                                                             height=30)
        browse_button.canvas.place(x=10, y=10)

        debug.log("[4/4] Browse Button created!", text_color="magenta")

        # Label for showing opened file path
        debug.log("[4/5] Creating file path Label...", text_color="magenta")
        opened_file_label = Label(button_wrapper,
                                  textvariable=self.selected_file_path,
                                  bg=BGCOLOR,
                                  font=("Helvetica", TIME_FONT_SIZE),
                                  wraplength=520,
                                  justify="left")
        # Place right to the button, vertically centered
        opened_file_label.place(x=browse_button.winfo_reqwidth() * 2 - 55,
                                y=browse_button.winfo_reqheight() / 2 - 5)
        debug.log("[4/6] File path Label created!", text_color="magenta")

    def browse_files(self):
        # Open a file dialog and get the selected file path
        debug.log("Opening file browser dialog...", text_color="magenta")
        file_path = filedialog.askopenfilename(title="Select a file",
                                               filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv"),
                                                          ("Image Files", "*.png;*.jpg;*.jpeg;*.gif"),
                                                          ("Text Files", "*.txt"),
                                                          ("All Files", "*.*")])

        global video_file_path
        video_file_path = file_path

        # Update the label with the selected file path
        self.selected_file_path.set(file_path)
        debug.log(f"Selected file: {file_path}", text_color="blue")
        if file_path:
            self.show_first_frame_details(file_path)
        else:
            debug.log("No file selected", text_color="red")

    def show_first_frame_details(self, path: str):
        """
        Display video details, including the first frame, in a labeled frame.

        Parameters:
        - path (str): The path to the video file.

        This method creates a labeled frame containing the first frame of the video and details about the video.
        The video details include the width, height, framerate, and bitrate.
        """

        # Creating a labeled frame to contain video details
        debug.log("[5/1] Creating video details wrapper...", text_color="yellow")
        frame_wrapper = LabelFrame(self.win,
                                   text="Video Data",
                                   bg=BGCOLOR,
                                   width=780,
                                   height=320,
                                   font=("Helvetica", 10, "bold"))
        frame_wrapper.place(x=10, y=100)
        debug.log("[5/2] Video details wrapper created!", text_color="yellow")

        # Creating a label to display the first frame of the video
        debug.log("[5/3] Creating placeholder label for first frame...", text_color="yellow")
        frame_label = Label(frame_wrapper)
        frame_label.place(x=5, y=5)
        debug.log("[5/4] First frame placeholder created!", text_color="yellow")

        # Opening the video and extracting details from the first frame
        debug.log("[5/5] Opening video file and getting first frame data...", text_color="yellow")
        cap = cv2.VideoCapture(path)
        fps = "{:.0f}".format(cap.get(cv2.CAP_PROP_FPS))
        bitrate = "{:.0f}".format(cap.get(cv2.CAP_PROP_BITRATE))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = "{:.0f}s".format(frame_count / int(fps))
        ret, frame = cap.read()
        cap.release()
        debug.log("[5/6] First frame data gathered!", text_color="yellow")

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)

            # Extracting video details from the first frame
            width, height = image.size
            aspect_ratio = width / height
            im_det = (f"Width: {image.width}px\n"
                      f"Height: {image.height}px\n"
                      f"Frames: {frame_count}\n"
                      f"Duration: {duration}\n"
                      f"Framerate: {fps} fps\n"
                      f"Bitrate: {bitrate} kbps")

            # Resizing the first frame to fit within the frame wrapper
            debug.log("[5/7] Calculating first frame information...", text_color="yellow")
            new_width = frame_wrapper.winfo_reqwidth() // 2
            new_height = int(new_width / aspect_ratio)
            image = image.resize((new_width, new_height), Image.BILINEAR)
            image_file = ImageTk.PhotoImage(image)
            debug.log("[5/8] First image information set!", text_color="yellow")

            # Configuring the frame label with the resized first frame
            debug.log("[5/9] Configuring image...", text_color="yellow")
            frame_label.config(image=image_file)
            frame_label.image = image_file
            debug.log("[5/10] Image configured!", text_color="yellow")

        # media_player_button = Button(frame_wrapper, text="Open Media Player")
        media_player_button = custom_button.RoundedRectangleButton(frame_wrapper,
                                                                   text="Open in VLC",
                                                                   width=110,
                                                                   height=30,
                                                                   # command=lambda: self.open_media_player(path))
                                                                   command=lambda: vlc_handler.open_video(path))
        media_player_button.canvas.place(x=10,
                                         y=new_height + 21)

        process_video_button = custom_button.RoundedRectangleButton(frame_wrapper,
                                                                    text="Process Video",
                                                                    width=110,
                                                                    height=30,
                                                                    command=lambda: self.process_video())
        process_video_button.canvas.place(x=media_player_button.winfo_reqwidth() + 20, y=new_height + 21)

        # Creating labels to display video details
        debug.log("[5/11] Creating labels to display video details...", text_color="yellow")
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
        debug.log("[5/12] Labels to display video details created!", text_color="yellow")

    def process_video(self):
        self.create_progress_bar()
        # processing.process_video(video_file_path, self.update_progress_bar)
        processing.set_progress_callback(self.update_progress)
        processing.process_video_thread(video_file_path)

    def create_progress_bar(self):
        progress_wrapper = LabelFrame(self.win,
                                      text="Progress",
                                      width=780,
                                      height=70,
                                      bg=BGCOLOR,
                                      font=("Helvetica", 10, "bold"))
        progress_wrapper.place(x=10, y=420)

        self.progress_bar = Progressbar(progress_wrapper,
                                        orient="horizontal",
                                        length=progress_wrapper.winfo_reqwidth() - 75,
                                        mode="determinate",
                                        maximum=100)
        self.progress_bar.place(x=5, y=5)

        self.progress_label = Label(progress_wrapper, text="100.00%", bg=BGCOLOR, font=("Helvetica", 10))
        self.progress_label.place(x=self.progress_bar.winfo_reqwidth() + 10, y=5)

    def update_progress(self, value):
        global call_nr
        call_nr += 1
        self.progress_bar['value'] = value
        self.progress_label['text'] = str(value + "%")
        # debug.log(f"Nr of calls: {call_nr}")
