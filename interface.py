import threading
from tkinter import Tk, Label, LabelFrame, StringVar, filedialog, Toplevel, OptionMenu, font
from tkinter.ttk import Progressbar

import cv2

from PIL import Image, ImageTk
from datetime import datetime

import config
import debug

import custom_button
import lang
import processing
import vlc_handler

# Global properties
BGCOLOR = "#3a3a3a"
WHITE = "#ffffff"
BLACK = "#000000"

FONT_COLOR = "#ffffff"
TIME_FONT_SIZE = 12
BIG_FONT_SIZE = 14
# FONT = ("Helvetica", TIME_FONT_SIZE)
# BOLD_FONT = ("Helvetica", TIME_FONT_SIZE, "bold")
FONT = ("Ubuntu", TIME_FONT_SIZE)
BOLD_FONT = ("Ubuntu", TIME_FONT_SIZE, "bold")
BIG_FONT = ("Ubuntu", BIG_FONT_SIZE)
BIG_FONT_BOLD = ("Ubuntu", BIG_FONT_SIZE, "bold")

TIME_WRAPPER_WIDTH = 100
TIME_WRAPPER_HEIGHT = 80
WIN_WIDTH = 800
WIN_HEIGHT = 500
FIN_WIN_WIDTH = 300
FIN_WIN_HEIGHT = 180
SET_WIN_WIDTH = 300
SET_WIN_HEIGHT = 300

call_nr = 0
video_file_path = None
prev_video_path = None


class Interface:
    def __init__(self):
        self.im_det = None
        self.ok_button = None
        self.finished_window = None
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
        self.settings = config.load_settings()
        self.curr_lang = self.settings[0]
        self.curr_theme = self.settings[1]

        global BGCOLOR, FONT_COLOR
        if self.curr_theme == "dark":
            BGCOLOR = "#3a3a3a"
            FONT_COLOR = "#ffffff"
        elif self.curr_theme == "light":
            BGCOLOR = WHITE
            FONT_COLOR = "#000000"

        debug.log("[1/1] Creating interface...", text_color="blue")

        # self.lang = lang.load_lang("hungarian")
        self.lang = lang.load_lang(self.curr_lang)

        self.set_properties()
        self.create_settings_button()
        self.create_time_frame()
        self.create_browser()

        debug.log("[1/2] Interface created", text_color="blue")

        self.win.mainloop()

    def create_font(self):
        global FONT
        font_file = "assets/fonts/Ubuntu-Regular.ttf"
        FONT = font.Font(family="Ubuntu", file=font_file, size=10)

    def set_properties(self):
        # Set windows properties
        debug.log("[2/1] Setting properties...", text_color="magenta")

        self.win = Tk()
        self.win["bg"] = BGCOLOR
        self.win.title(self.lang["title"])
        self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW")
        self.selected_file_path = StringVar()
        # self.create_font()
        debug.log("[2/2] Properties set!", text_color="magenta")

    def create_settings_button(self):
        self.settings_button = custom_button.CustomButton(self.win,
                                                          command=self.create_settings_window,
                                                          button_type=custom_button.settings_button,
                                                          bg=BGCOLOR)
        self.settings_button.canvas.place(x=10, y=20)

    def update_label(self):
        # Update the label text with the current time
        self.time_label.config(text=datetime.now().strftime("%H:%M:%S"))
        # Schedule the update_label method to be called again after 1000 milliseconds
        self.win.after(1000, self.update_label)

    def create_time_frame(self):
        # Wrapper for time Label
        debug.log("[3/1] Creating Time Frame wrapper...", text_color="yellow")

        self.time_wrapper = LabelFrame(self.win,
                                       text=self.lang["time"],
                                       width=TIME_WRAPPER_WIDTH,
                                       height=TIME_WRAPPER_HEIGHT,
                                       bg=BGCOLOR,
                                       fg=FONT_COLOR)

        self.time_wrapper.place(x=83, y=5)

        debug.log("[3/2] Time wrapper created!", text_color="yellow")

        # Label that shows the current time and date
        debug.log("[3/3] Creating Time Label...", text_color="yellow")

        self.time_label = Label(self.time_wrapper, text=datetime.now().strftime("%H:%M:%S"))
        self.time_label.config(font=("Ubuntu", 10),  # Font size
                               fg=FONT_COLOR,  # Font color
                               bg=BGCOLOR)  # Background color

        debug.log("[3/4] Time Label created!", text_color="yellow")

        # Set Frame label to width and height of Label
        debug.log("[3/5] Updating Time Label config...", text_color="yellow")
        self.time_wrapper.config(font=BOLD_FONT,
                                 width=self.time_label.winfo_reqwidth() + 20)
        debug.log("[3/6] Time Label config updated!", text_color="yellow")

        # Pack Label in Frame
        debug.log("[3/7] Packing Time Label in Frame...", text_color="yellow")
        # self.time_label.pack(padx=10,
        #                      pady=5,
        #                      anchor="center")
        self.time_label.place(x=self.time_label.winfo_reqwidth() // 6,
                              y=self.time_wrapper.winfo_reqheight() // 2 - self.time_label.winfo_reqheight())
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
                                    font=BOLD_FONT)
        # Place to the right
        x_coordinate = WIN_WIDTH - button_wrapper.winfo_reqwidth() - 10
        button_wrapper.place(x=x_coordinate, y=5)
        debug.log("[4/2] Browsing wrapper created!", text_color="magenta")

        # Button to initiate browsing
        debug.log("[4/3] Creating browse Button...", text_color="magenta")

        self.browse_button = custom_button.CustomButton(button_wrapper,
                                                        text=self.lang["browse"],
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
                                       font=FONT,
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
                                   text=self.lang["video_data"],
                                   fg=FONT_COLOR,
                                   bg=BGCOLOR,
                                   width=780,
                                   height=320,
                                   font=BOLD_FONT)
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
            self.im_det = (f"{self.lang["width"]}: {image.width}px\n"
                           f"{self.lang["height"]}: {image.height}px\n"
                           f"{self.lang["frames"]}: {frame_count}\n"
                           f"{self.lang["duration"]}: {duration}\n"
                           f"{self.lang["framerate"]}: {fps} fps\n"
                           f"{self.lang["bitrate"]}: {bitrate} kbps")

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
                                                         text=self.lang["open_vlc"],
                                                         bg=BGCOLOR,
                                                         width=110,
                                                         height=30,
                                                         # command=lambda: self.open_media_player(path))
                                                         command=lambda: vlc_handler.open_video(path))
        media_player_button.canvas.place(x=10,
                                         y=new_height + 21)

        self.process_video_button = custom_button.CustomButton(frame_wrapper,
                                                               text=self.lang["process"],
                                                               bg=BGCOLOR,
                                                               width=110,
                                                               height=30,
                                                               command=lambda: self.process_video())
        self.process_video_button.canvas.place(x=media_player_button.winfo_reqwidth() + 20, y=new_height + 21)

        # Creating labels to display video details
        debug.log("[5/11] Creating labels to display video details...", text_color="yellow")
        frame_details_header = Label(frame_wrapper,
                                     text=self.lang["video_det"],
                                     fg=FONT_COLOR,
                                     bg=BGCOLOR,
                                     font=BIG_FONT_BOLD)
        frame_details_header.place(x=new_width + 30, y=10)
        image_details = Label(frame_wrapper,
                              text=self.im_det,
                              fg=FONT_COLOR,
                              bg=BGCOLOR,
                              font=FONT,
                              # Left alignment
                              justify="left",
                              anchor="w"
                              )
        image_details.place(x=new_width + 30, y=frame_details_header.winfo_reqheight() + 5)
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
                                      text=self.lang["progress"],
                                      width=780,
                                      height=70,
                                      fg=FONT_COLOR,
                                      bg=BGCOLOR,
                                      font=BOLD_FONT)
        progress_wrapper.place(x=10, y=420)

        self.progress_bar = Progressbar(progress_wrapper,
                                        orient="horizontal",
                                        length=progress_wrapper.winfo_reqwidth() - 75,
                                        mode="determinate",
                                        maximum=100)
        self.progress_bar.place(x=5, y=5)

        self.progress_label = Label(progress_wrapper, text="100.00%", fg=FONT_COLOR, bg=BGCOLOR, font=("Ubuntu", 10))
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
        self.finished_window = Toplevel(self.win)
        self.finished_window.title(self.lang["result_win_title"])
        self.finished_window.geometry(str(FIN_WIN_WIDTH) + "x" + str(FIN_WIN_HEIGHT))
        self.finished_window.configure(background=BGCOLOR)
        self.finished_window.resizable(False, False)

        # Centering finished window on screen
        screen_width = self.finished_window.winfo_screenwidth()
        screen_height = self.finished_window.winfo_screenheight()
        x = (screen_width - FIN_WIN_WIDTH) // 2
        y = (screen_height - FIN_WIN_HEIGHT) // 2
        self.finished_window.geometry(f"+{x}+{y}")

        title_label = Label(self.finished_window,
                            text=self.lang["proc_finished"],
                            fg=FONT_COLOR,
                            bg=BGCOLOR,
                            font=BOLD_FONT)
        title_label.pack(pady=20)

        result_label = Label(self.finished_window,
                             text=processing.total_difference,
                             fg=FONT_COLOR,
                             bg=BGCOLOR,
                             font=FONT)
        result_label.pack(pady=0)

        # This gives error when clicked
        self.ok_button = custom_button.CustomButton(self.finished_window,
                                                    text=self.lang["ok"],
                                                    bg=BGCOLOR,
                                                    command=self.close_finished_windows,
                                                    button_type=custom_button.button)
        self.ok_button.canvas.pack(pady=20)
        self.process_video_button.enable()
        self.browse_button.enable()

    def close_finished_windows(self):
        self.browse_button.enable()
        self.process_video_button.enable()
        self.ok_button.destroy()
        self.finished_window.destroy()
        debug.log("Finished window closed!", text_color="cyan")

    def create_settings_window(self):
        """
        Creates the settings window.

        This method creates a window where users can configure settings such as language and theme.

        Args:
            self: The instance of the Interface class.

        Returns:
            None
        """

        # Create the settings window
        settings_window = Toplevel(self.win)
        settings_window.title(self.lang["settings"])
        settings_window.geometry(f"{SET_WIN_WIDTH}x{SET_WIN_HEIGHT}")
        settings_window.configure(background=BGCOLOR)
        settings_window.resizable(False, False)

        # Add a label for the settings window title
        label = Label(settings_window,
                      text=self.lang["settings"],
                      fg=FONT_COLOR,
                      bg=BGCOLOR,
                      font=BOLD_FONT)
        label.pack(pady=10)

        # Add a label for the language selection
        lang_label = Label(settings_window,
                           text=self.lang["lang"],
                           fg=FONT_COLOR,
                           bg=BGCOLOR,
                           font=FONT,
                           anchor="center")
        lang_label.place(x=SET_WIN_WIDTH // 2 - lang_label.winfo_reqwidth() - 20, y=label.winfo_reqheight() + 25)

        # Define language options
        lang_options = [self.lang["english"], self.lang["hungarian"]]

        # Set default language option based on current language setting
        lang_selected_option = StringVar(settings_window)
        lang_selected_option.set(lang_options[1] if self.curr_lang == "hungarian" else lang_options[0])

        # Add language OptionMenu
        lang_option_menu = OptionMenu(settings_window, lang_selected_option, *lang_options)
        lang_option_menu.config(anchor="center")
        lang_option_menu.place(x=SET_WIN_WIDTH // 2 + 10, y=lang_label.winfo_reqheight() * 2)

        # Add a label for the theme selection
        theme_label = Label(settings_window,
                            text=self.lang["theme"],
                            fg=FONT_COLOR,
                            bg=BGCOLOR,
                            font=FONT,
                            anchor="center")
        theme_label.place(x=SET_WIN_WIDTH // 2 - theme_label.winfo_reqwidth() - 30, y=lang_label.winfo_reqheight() * 4)

        # Define theme options
        theme_options = [self.lang["dark"], self.lang["light"]]

        # Set default theme option based on current theme setting
        theme_selected_option = StringVar(settings_window)
        theme_selected_option.set(theme_options[0] if self.curr_theme == "dark" else theme_options[1])

        # Add theme OptionMenu
        theme_option_menu = OptionMenu(settings_window, theme_selected_option, *theme_options)
        theme_option_menu.config(anchor="center")
        theme_option_menu.place(x=SET_WIN_WIDTH // 2 + 10, y=lang_label.winfo_reqheight() * 4)

        def save_option():
            """
            Saves the selected language and theme options.

            This function retrieves the selected language and theme options from the OptionMenu widgets
            and saves them to the configuration file. It also displays a message prompting the user to
            restart the program for the changes to take effect.
            """

            # Retrieve selected language option
            chosen_lang_option = lang_selected_option.get()

            # Map language options to standard format
            chosen_lang_option = "hungarian" if chosen_lang_option in ("Magyar", "Hungarian") else "english"

            # Retrieve selected theme option
            chosen_theme_option = theme_selected_option.get()

            # Map theme options to standard format
            chosen_theme_option = "dark" if chosen_theme_option in ("Sötét", "Dark") else "light"

            # Display restart message if settings have changed
            if chosen_lang_option != self.curr_lang or chosen_theme_option != self.curr_theme:
                restart_label = Label(settings_window,
                                      text=self.lang["restart"],
                                      fg="#ff5b19",
                                      bg=BGCOLOR)
                restart_label.place(x=settings_window.winfo_reqwidth() // 2, y=200)

            # Save selected options to configuration file
            debug.log(f"Settings - Language: {chosen_lang_option}, Theme: {chosen_theme_option}")
            config.save_settings([chosen_lang_option, chosen_theme_option])

        # Add a button to save the selected options
        save_button = custom_button.CustomButton(settings_window,
                                                 text=self.lang["save"],
                                                 command=save_option,
                                                 button_type=custom_button.button,
                                                 bg=BGCOLOR)
        save_button.canvas.pack(pady=100)
