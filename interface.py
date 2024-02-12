import threading
from tkinter import Tk, Label, LabelFrame, Button, StringVar, filedialog, PhotoImage, Toplevel
from tkinter.ttk import Progressbar

import cv2

from PIL import Image, ImageTk
from datetime import datetime

import debug

import custom_button
import processing
import vlc_handler

# Global properties
# BGCOLOR = "#00b685"
BGCOLOR = "#3a3a3a"
WHITE = "#ffffff"
BLACK = "#000000"
FONT_COLOR = "#ffffff"

TIME_FONT_SIZE = 10
TIME_WRAPPER_WIDTH = 100
TIME_WRAPPER_HEIGHT = 80
WIN_WIDTH = 800
WIN_HEIGHT = 500
FIN_WIN_WIDTH = 300
FIN_WIN_HEIGHT = 180
call_nr = 0
video_file_path = None
prev_video_path = None


class Interface:
    def __init__(self):
        self.settings_wrapper = None
        self.selected_file_path = None
        self.win = None
        self.time_label = None
        self.time_wrapper = None
        self.progress_bar = None
        self.progress_label = None
        self.process_video_button = None
        self.browse_button = None
        self.is_file_selected = False
        self.opened_file_label = None
        self.settings_button = None

        debug.log("[1/1] Creating interface...", text_color="blue")

        self.set_properties()
        self.create_settings_button()
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

    def create_settings_button(self):
        # self.settings_wrapper = LabelFrame(self.win,
        #                                    text="Settings",
        #                                    width=66,
        #                                    height=80,
        #                                    bg=BGCOLOR,
        #                                    font=("Helvetica", TIME_FONT_SIZE, "bold"))
        # # self.settings_wrapper.place(x=10, y=5)

        self.settings_button = custom_button.CustomButton(self.win,
                                                          command=self.print_test,
                                                          button_type=custom_button.settings_button,
                                                          bg=BGCOLOR)
        self.settings_button.canvas.place(x=10, y=20)

    def print_test(self):
        print("Clicked!")

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)

    def create_time_frame(self):
        # Wrapper for time Label
        debug.log("[3/1] Creating Time Frame wrapper...", text_color="yellow")

        self.time_wrapper = LabelFrame(self.win,
                                       text="Time",
                                       width=TIME_WRAPPER_WIDTH,
                                       height=TIME_WRAPPER_HEIGHT,
                                       bg=BGCOLOR,
                                       fg=FONT_COLOR)

        self.time_wrapper.place(x=83, y=5)

        debug.log("[3/2] Time wrapper created!", text_color="yellow")

        # Label that shows the current time and date
        debug.log("[3/3] Creating Time Label...", text_color="yellow")

        self.time_label = Label(self.time_wrapper, text=datetime.now().strftime("%H:%M:%S"))
        self.time_label.config(font=("Helvetica", TIME_FONT_SIZE),  # Font size
                               fg=FONT_COLOR,  # Font color
                               bg=BGCOLOR)  # Background color

        debug.log("[3/4] Time Label created!", text_color="yellow")

        # Set Frame label to width and height of Label
        debug.log("[3/5] Updating Time Label config...", text_color="yellow")
        label_width = self.time_label.winfo_reqwidth() + 20
        label_height = self.time_label.winfo_reqheight() * 2
        self.time_wrapper.config(font=("Helvetica", TIME_FONT_SIZE, "bold"),
                                 width=label_width)
        debug.log("[3/6] Time Label config updated!", text_color="yellow")

        # Pack Label in Frame
        debug.log("[3/7] Packing Time Label in Frame...", text_color="yellow")
        # self.time_label.pack(padx=10,
        #                      pady=5,
        #                      anchor="center")
        self.time_label.place(x=10, y=5)
        debug.log("[3/8] Time Label packed!", text_color="yellow")
        # Schedule the update_label method to be called
        self.win.after(1000, self.update_label)

    def run_browser_on_thread(self):
        # Run the file browser on a separate thread
        file_browser_thread = threading.Thread(target=self.create_browser)
        file_browser_thread.start()

    def create_browser(self):
        # Wrapper for file browsing
        debug.log("[4/1] Creating Browsing wrapper...", text_color="magenta")
        button_wrapper = LabelFrame(self.win,
                                    text="Input file",
                                    fg=FONT_COLOR,
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

        self.browse_button = custom_button.CustomButton(button_wrapper,
                                                        text="Browse",
                                                        command=self.browse_files,
                                                        width=70,
                                                        height=30,
                                                        button_type=custom_button.button,
                                                        bg=BGCOLOR)
        self.browse_button.canvas.place(x=10, y=10)

        debug.log("[4/4] Browse Button created!", text_color="magenta")

        # Label for showing opened file path
        debug.log("[4/5] Creating file path Label...", text_color="magenta")
        self.opened_file_label = Label(button_wrapper,
                                       textvariable=self.selected_file_path,
                                       fg=FONT_COLOR,
                                       bg=BGCOLOR,
                                       font=("Helvetica", TIME_FONT_SIZE),
                                       wraplength=520,
                                       justify="left")
        # Place right to the button, vertically centered
        self.opened_file_label.place(x=self.browse_button.winfo_reqwidth() * 2 - 55,
                                     y=self.browse_button.winfo_reqheight() / 2 - 5)
        debug.log("[4/6] File path Label created!", text_color="magenta")

    def browse_files(self):
        # Open a file dialog and get the selected file path
        global video_file_path
        global prev_video_path
        video_file_path = prev_video_path
        debug.log("Opening file browser dialog...", text_color="magenta")
        file_path = filedialog.askopenfilename(title="Select a file",
                                               filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv")])

        # Update the label with the selected file path
        if file_path:
            self.selected_file_path.set(file_path)
            debug.log(f"Selected file: {file_path}", text_color="blue")
            self.show_first_frame_details(file_path)
            video_file_path = file_path
            prev_video_path = video_file_path
        else:
            debug.log("No file selected", text_color="red")
            if prev_video_path:
                debug.log("Selecting previous video", text_color="blue")
                self.opened_file_label.config(text=prev_video_path)
                self.show_first_frame_details(prev_video_path)

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
                                   fg=FONT_COLOR,
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
        media_player_button = custom_button.CustomButton(frame_wrapper,
                                                         text="Open in VLC",
                                                         bg=BGCOLOR,
                                                         width=110,
                                                         height=30,
                                                         # command=lambda: self.open_media_player(path))
                                                         command=lambda: vlc_handler.open_video(path))
        media_player_button.canvas.place(x=10,
                                         y=new_height + 21)

        self.process_video_button = custom_button.CustomButton(frame_wrapper,
                                                               text="Process Video",
                                                               bg=BGCOLOR,
                                                               width=110,
                                                               height=30,
                                                               command=lambda: self.process_video())
        self.process_video_button.canvas.place(x=media_player_button.winfo_reqwidth() + 20, y=new_height + 21)

        # Creating labels to display video details
        debug.log("[5/11] Creating labels to display video details...", text_color="yellow")
        frame_details_header = Label(frame_wrapper,
                                     text="Video details:",
                                     fg=FONT_COLOR,
                                     bg=BGCOLOR,
                                     font=("Helvetica", 10, "bold")
                                     )
        frame_details_header.place(x=new_width + 30, y=10)
        image_details = Label(frame_wrapper,
                              text=im_det,
                              fg=FONT_COLOR,
                              bg=BGCOLOR,
                              font=("Helvetica", 10),
                              # Left alignment
                              justify="left",
                              anchor="w"
                              )
        image_details.place(x=new_width + 30, y=frame_details_header.winfo_reqheight() * 1.5)
        debug.log("[5/12] Labels to display video details created!", text_color="yellow")

    def process_video(self):
        if video_file_path:
            self.process_video_button.disable()
            self.browse_button.disable()
            self.create_progress_bar()
            # processing.process_video(video_file_path, self.update_progress_bar)
            processing.set_progress_callback(self.update_progress)
            processing.process_video_thread(video_file_path)

    def create_progress_bar(self):
        progress_wrapper = LabelFrame(self.win,
                                      text="Progress",
                                      width=780,
                                      height=70,
                                      fg=FONT_COLOR,
                                      bg=BGCOLOR,
                                      font=("Helvetica", 10, "bold"))
        progress_wrapper.place(x=10, y=420)

        self.progress_bar = Progressbar(progress_wrapper,
                                        orient="horizontal",
                                        length=progress_wrapper.winfo_reqwidth() - 75,
                                        mode="determinate",
                                        maximum=100)
        self.progress_bar.place(x=5, y=5)

        self.progress_label = Label(progress_wrapper, text="100.00%", fg=FONT_COLOR, bg=BGCOLOR, font=("Helvetica", 10))
        self.progress_label.place(x=self.progress_bar.winfo_reqwidth() + 10, y=5)

    def update_progress(self, value):
        global call_nr
        call_nr += 1
        self.progress_bar['value'] = value
        self.progress_label['text'] = str(value + "%")
        # debug.log(f"Nr of calls: {call_nr}")
        if processing.finished:
            debug.log(processing.total_difference)
            self.create_finished_window()

    def create_finished_window(self):
        finished_window = Toplevel(self.win)
        finished_window.title("Processing result")
        finished_window.geometry(str(FIN_WIN_WIDTH) + "x" + str(FIN_WIN_HEIGHT))
        finished_window.configure(background=BGCOLOR)
        finished_window.resizable(False, False)

        # Centering finished window on screen
        screen_width = finished_window.winfo_screenwidth()
        screen_height = finished_window.winfo_screenheight()
        x = (screen_width - FIN_WIN_WIDTH) // 2
        y = (screen_height - FIN_WIN_HEIGHT) // 2
        finished_window.geometry(f"+{x}+{y}")

        title_label = Label(finished_window,
                            text="Processing finished!",
                            fg=FONT_COLOR,
                            bg=BGCOLOR,
                            font=("Helvetica", 10, "bold"))
        title_label.pack(pady=20)

        result_label = Label(finished_window,
                             text=processing.total_difference,
                             fg=FONT_COLOR,
                             bg=BGCOLOR,
                             font=("Helvetica", 10))
        result_label.pack(pady=0)

        # This gives error when clicked
        ok_button = custom_button.CustomButton(finished_window,
                                               text="OK",
                                               bg=BGCOLOR,
                                               command=finished_window.destroy,
                                               button_type=custom_button.button)
        ok_button.canvas.pack(pady=20)
        self.process_video_button.enable()
        self.browse_button.enable()
