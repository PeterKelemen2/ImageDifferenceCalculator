import threading
from tkinter import Tk, Label, LabelFrame, StringVar, filedialog, Toplevel, OptionMenu, font, Button
from tkinter.ttk import Progressbar

import cv2

from PIL import Image, ImageTk
from datetime import datetime

import config
import custom_ui

import debug

import custom_button
import lang
import processing
import vlc_handler

# Global properties
BGCOLOR = "#3a3a3a"
DARKER_BG = "#292929"
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
HIS_WIN_WIDTH = 900
HIS_WIN_HEIGHT = 800

call_nr = 0
video_file_path = None
prev_video_path = None


class Interface:
    def __init__(self):
        self.next_lang = None
        self.previous_language = None
        self.prev_lang_dict = None
        self.eng_dict = lang.load_lang("english")
        self.hun_dict = lang.load_lang("hungarian")
        self.history_content_list = list()
        self.outline_frame = None
        self.history_exit_button = None
        self.history_title = None
        self.history_label = None
        self.history_text = None
        self.history_window = None
        self.history_button = None
        self.result_label = None
        self.finished_title_label = None
        self.save_button = None
        self.lang_label = None
        self.theme_label = None
        self.lang_selected_option = None
        self.lang_options = None
        self.label = None
        self.settings_window = None
        self.progress_wrapper = None
        self.media_player_button = None
        self.image_details = None
        self.frame_details_header = None
        self.frame_wrapper = None
        self.button_wrapper = None
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
        self.image_detail_dict = None

        self.rounded_label_frame = None
        self.new_button = None

        self.set_color()

        debug.log("[1/1] Creating interface...", text_color="blue")

        # self.lang = lang.load_lang("hungarian")
        self.lang = lang.load_lang(self.curr_lang)

        self.set_properties()
        self.create_settings_button()
        self.create_history_button()
        # self.create_time_frame()
        self.create_browser()

        debug.log("[1/2] Interface created", text_color="blue")

        # self.rounded_label_frame = custom_ui.CustomLabelFrame(self.win, text=self.lang["input_file"], width=620,
        #                                                       height=80,
        #                                                       radius=15)
        # self.rounded_label_frame.canvas.place(x=170, y=10)
        #
        # self.new_button = custom_button.CustomButton(self.rounded_label_frame.canvas, text="Gonb", bg=BLACK,
        #                                              button_type=custom_button.button)
        # self.new_button.canvas.place(x=10, y=30)

        self.win.mainloop()

    def create_font(self):
        global FONT
        font_file = "assets/fonts/Ubuntu-Regular.ttf"
        FONT = font.Font(family="Ubuntu", file=font_file, size=10)

    def set_color(self):
        global BGCOLOR, FONT_COLOR, DARKER_BG
        if self.curr_theme == "dark":
            BGCOLOR = "#3a3a3a"
            FONT_COLOR = "#ffffff"
            DARKER_BG = "#292929"
        elif self.curr_theme == "light":
            BGCOLOR = WHITE
            FONT_COLOR = "#000000"
            DARKER_BG = "#e6e6e6"

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

    def create_history_button(self):
        self.history_button = custom_button.CustomButton(self.win,
                                                         command=lambda: self.create_history_window(),
                                                         button_type=custom_button.history_button,
                                                         bg=BGCOLOR)
        self.history_button.canvas.place(x=self.settings_button.winfo_reqheight() + 30, y=20)

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
        self.button_wrapper = LabelFrame(self.win,
                                         text=self.lang["input_file"],
                                         fg=FONT_COLOR,
                                         bg=BGCOLOR,
                                         width=620,
                                         height=80,
                                         font=BOLD_FONT)
        # Place to the right
        x_coordinate = WIN_WIDTH - self.button_wrapper.winfo_reqwidth() - 10
        # self.button_wrapper.place(x=x_coordinate, y=5)
        debug.log("[4/2] Browsing wrapper created!", text_color="magenta")

        # Button to initiate browsing
        debug.log("[4/3] Creating browse Button...", text_color="magenta")

        self.browse_button = custom_button.CustomButton(self.button_wrapper,
                                                        text=self.lang["browse"],
                                                        command=self.browse_files,
                                                        width=70,
                                                        height=30,
                                                        button_type=custom_button.button,
                                                        bg=BGCOLOR)
        # self.browse_button.canvas.place(x=10, y=10)

        self.rounded_label_frame = custom_ui.CustomLabelFrame(self.win, text=self.lang["input_file"], width=620,
                                                              height=80,
                                                              radius=15)
        self.rounded_label_frame.canvas.place(x=170, y=10)

        self.new_button = custom_button.CustomButton(self.rounded_label_frame.canvas, text="Gonb", bg=BLACK,
                                                     button_type=custom_button.button)
        self.new_button.canvas.place(x=10, y=30)


        debug.log("[4/4] Browse Button created!", text_color="magenta")

        # Label for showing opened file path
        debug.log("[4/5] Creating file path Label...", text_color="magenta")
        self.opened_file_label = Label(self.button_wrapper,
                                       textvariable=self.selected_file_path,
                                       fg=FONT_COLOR,
                                       bg=BGCOLOR,
                                       font=FONT,
                                       wraplength=520,
                                       justify="left")
        self.opened_file_label.config(text=self.lang["None"], anchor="center")
        # Place right to the button, vertically centered
        self.opened_file_label.place(x=self.browse_button.winfo_reqwidth() * 2 - 55,
                                     y=self.button_wrapper.winfo_reqheight() // 2 - self.opened_file_label.winfo_reqheight() * 1.5)
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
        self.frame_wrapper = LabelFrame(self.win,
                                        text=self.lang["video_data"],
                                        fg=FONT_COLOR,
                                        bg=BGCOLOR,
                                        width=780,
                                        height=320,
                                        font=BOLD_FONT)
        self.frame_wrapper.place(x=10, y=100)
        debug.log("[5/2] Video details wrapper created!", text_color="yellow")

        # Creating a label to display the first frame of the video
        debug.log("[5/3] Creating placeholder label for first frame...", text_color="yellow")
        frame_label = Label(self.frame_wrapper)
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
            self.image_detail_dict = {
                "width": f"{image.width}px",
                "height": f"{image.height}px",
                "frames": f"{frame_count}",
                "duration": str("{:.0f}s".format(frame_count / int(fps))),
                "framerate": f"{fps} fps",
                "bitrate": f"{bitrate} kbps"
            }
            self.im_det = (f"{self.lang["width"]}: {image.width}px\n"
                           f"{self.lang["height"]}: {image.height}px\n"
                           f"{self.lang["frames"]}: {frame_count}\n"
                           f"{self.lang["duration"]}: {duration}\n"
                           f"{self.lang["framerate"]}: {fps} fps\n"
                           f"{self.lang["bitrate"]}: {bitrate} kbps")

            # Resizing the first frame to fit within the frame wrapper
            debug.log("[5/7] Calculating first frame information...", text_color="yellow")
            new_width = self.frame_wrapper.winfo_reqwidth() // 2
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
        self.media_player_button = custom_button.CustomButton(self.frame_wrapper,
                                                              text=self.lang["open_vlc"],
                                                              bg=BGCOLOR,
                                                              width=110,
                                                              height=30,
                                                              # command=lambda: self.open_media_player(path))
                                                              command=lambda: vlc_handler.open_video(path))
        self.media_player_button.canvas.place(x=10,
                                              y=new_height + 21)

        self.process_video_button = custom_button.CustomButton(self.frame_wrapper,
                                                               text=self.lang["process"],
                                                               bg=BGCOLOR,
                                                               width=110,
                                                               height=30,
                                                               command=lambda: self.process_video())
        self.process_video_button.canvas.place(x=self.media_player_button.winfo_reqwidth() + 20, y=new_height + 21)

        # Creating labels to display video details
        debug.log("[5/11] Creating labels to display video details...", text_color="yellow")
        self.frame_details_header = Label(self.frame_wrapper,
                                          text=self.lang["video_det"],
                                          fg=FONT_COLOR,
                                          bg=BGCOLOR,
                                          font=BIG_FONT_BOLD)
        self.frame_details_header.place(x=new_width + 30, y=10)
        self.image_details = Label(self.frame_wrapper,
                                   text=self.im_det,
                                   fg=FONT_COLOR,
                                   bg=BGCOLOR,
                                   font=FONT,
                                   # Left alignment
                                   justify="left",
                                   anchor="w"
                                   )
        self.image_details.place(x=new_width + 30, y=self.frame_details_header.winfo_reqheight() + 5)
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
        self.progress_wrapper = LabelFrame(self.win,
                                           text=self.lang["progress"],
                                           width=780,
                                           height=70,
                                           fg=FONT_COLOR,
                                           bg=BGCOLOR,
                                           font=BOLD_FONT)
        self.progress_wrapper.place(x=10, y=420)

        self.progress_bar = Progressbar(self.progress_wrapper,
                                        orient="horizontal",
                                        length=self.progress_wrapper.winfo_reqwidth() - 75,
                                        mode="determinate",
                                        maximum=100)
        self.progress_bar.place(x=5, y=5)

        self.progress_label = Label(self.progress_wrapper, text="100.00%", fg=FONT_COLOR, bg=BGCOLOR,
                                    font=("Ubuntu", 10))
        self.progress_label.place(x=self.progress_bar.winfo_reqwidth() + 10, y=5)

    def update_progress(self, value):
        global call_nr
        call_nr += 1
        self.progress_bar['value'] = value
        self.progress_label['text'] = str(value + "%")
        # debug.log(f"Nr of calls: {call_nr}")
        if processing.finished:
            debug.log(f"{self.lang["diff"]}: {processing.total_difference}", text_color="blue")
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

        self.finished_title_label = Label(self.finished_window,
                                          text=self.lang["proc_finished"],
                                          fg=FONT_COLOR,
                                          bg=BGCOLOR,
                                          font=BOLD_FONT)
        self.finished_title_label.pack(pady=20)

        self.result_label = Label(self.finished_window,
                                  text=f"{self.lang["diff"]}: {processing.total_difference}",
                                  fg=FONT_COLOR,
                                  bg=BGCOLOR,
                                  font=FONT)
        self.result_label.pack(pady=0)

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
        self.settings_window = Toplevel(self.win)
        self.settings_window.title(self.lang["settings"])
        self.settings_window.geometry(f"{SET_WIN_WIDTH}x{SET_WIN_HEIGHT}")
        self.settings_window.configure(background=BGCOLOR)
        self.settings_window.resizable(False, False)

        # Add a label for the settings window title
        self.label = Label(self.settings_window,
                           text=self.lang["settings"],
                           fg=FONT_COLOR,
                           bg=BGCOLOR,
                           font=BOLD_FONT)
        self.label.pack(pady=10)

        # Add a label for the language selection
        self.lang_label = Label(self.settings_window,
                                text=self.lang["lang"],
                                fg=FONT_COLOR,
                                bg=BGCOLOR,
                                font=FONT,
                                anchor="center")
        self.lang_label.place(x=SET_WIN_WIDTH // 4, y=self.label.winfo_reqheight() + 25)

        # Define language options
        self.lang_options = [self.lang["english"], self.lang["hungarian"]]

        # Set default language option based on current language setting
        self.lang_selected_option = StringVar(self.settings_window)
        self.lang_selected_option.set(self.lang_options[1] if self.curr_lang == "hungarian" else self.lang_options[0])

        # Add language OptionMenu
        lang_option_menu = OptionMenu(self.settings_window, self.lang_selected_option, *self.lang_options)
        lang_option_menu.config(anchor="center")
        lang_option_menu.place(x=SET_WIN_WIDTH // 2 + 10, y=self.lang_label.winfo_reqheight() * 2)

        # Add a label for the theme selection
        self.theme_label = Label(self.settings_window,
                                 text=self.lang["theme"],
                                 fg=FONT_COLOR,
                                 bg=BGCOLOR,
                                 font=FONT,
                                 anchor="center")
        self.theme_label.place(x=SET_WIN_WIDTH // 4, y=self.lang_label.winfo_reqheight() * 4)

        # Define theme options
        theme_options = [self.lang["dark"], self.lang["light"]]

        # Set default theme option based on current theme setting
        theme_selected_option = StringVar(self.settings_window)
        theme_selected_option.set(theme_options[0] if self.curr_theme == "dark" else theme_options[1])

        # Add theme OptionMenu
        theme_option_menu = OptionMenu(self.settings_window, theme_selected_option, *theme_options)
        theme_option_menu.config(anchor="center")
        theme_option_menu.place(x=SET_WIN_WIDTH // 2 + 10, y=self.lang_label.winfo_reqheight() * 4)

        def save_option():
            """
            Saves the selected language and theme options.

            This function retrieves the selected language and theme options from the OptionMenu widgets
            and saves them to the configuration file. It also displays a message prompting the user to
            restart the program for the changes to take effect.
            """

            # Retrieve selected language and theme option
            chosen_lang_option = self.lang_selected_option.get()
            chosen_theme_option = theme_selected_option.get()

            # Map language options to standard format
            chosen_lang_option = "hungarian" if chosen_lang_option in ("Magyar", "Hungarian") else "english"
            # Map theme options to standard format
            chosen_theme_option = "dark" if chosen_theme_option in ("Sötét", "Dark") else "light"

            if chosen_lang_option != self.curr_lang:
                print(self.curr_lang, chosen_lang_option)
                self.prev_lang_dict = lang.load_lang(self.curr_lang)
                self.next_lang = lang.load_lang(chosen_lang_option)

                self.lang = lang.load_lang(chosen_lang_option)
                self.curr_lang = chosen_lang_option
                self.change_language()

            if chosen_theme_option != self.curr_theme:
                self.curr_theme = chosen_theme_option
                print(self.curr_theme)
                self.update_colors()

            # Save selected options to configuration file
            debug.log(f"Settings - Language: {chosen_lang_option}, Theme: {chosen_theme_option}")
            config.save_settings([chosen_lang_option, chosen_theme_option])
            # self.update_text()

        # Add a button to save the selected options
        self.save_button = custom_button.CustomButton(self.settings_window,
                                                      text=self.lang["save"],
                                                      command=save_option,
                                                      button_type=custom_button.button,
                                                      bg=BGCOLOR)
        self.save_button.canvas.pack(pady=100)

    def create_history_window(self):
        history_list = processing.read_from_history()
        self.history_window = Toplevel(self.win)
        self.history_window.title(self.lang["history"])
        self.history_window.configure(background=BGCOLOR)
        self.history_window.resizable(False, False)

        self.history_title = Label(self.history_window,
                                   text=self.lang["history"],
                                   fg=FONT_COLOR,
                                   bg=BGCOLOR,
                                   font=BIG_FONT_BOLD)
        self.outline_frame = LabelFrame(self.history_window,
                                        bg=DARKER_BG)
        self.history_content_list = list()
        for line in history_list:
            new_line = line.split(";")
            self.history_content_list.append(Label(self.outline_frame,
                                                   text=new_line[0],
                                                   font=FONT,
                                                   wraplength=HIS_WIN_WIDTH - 40,
                                                   fg=FONT_COLOR,
                                                   bg=DARKER_BG))
            self.history_content_list[len(self.history_content_list) - 1].pack()

            self.history_content_list.append(Label(self.outline_frame,
                                                   text=new_line[1],
                                                   fg=FONT_COLOR,
                                                   bg=DARKER_BG,
                                                   font=BOLD_FONT))
            self.history_content_list[len(self.history_content_list) - 1].pack()

        self.history_title.pack(pady=10)
        self.outline_frame.pack(pady=5)

        self.history_exit_button = custom_button.CustomButton(self.history_window,
                                                              text=self.lang["exit"],
                                                              command=self.close_history_window,
                                                              button_type=custom_button.button,
                                                              bg=BGCOLOR)

        self.history_window.update_idletasks()
        self.history_window.geometry(f"{self.outline_frame.winfo_reqwidth() + 40}x{HIS_WIN_HEIGHT}")
        self.history_exit_button.canvas.place(
            x=self.history_window.winfo_width() // 2 - self.history_exit_button.winfo_reqwidth() // 4,
            y=HIS_WIN_HEIGHT - self.history_exit_button.winfo_reqheight() * 2)

    def close_history_window(self):
        if self.history_window is not None:
            self.history_exit_button.destroy()
            self.history_exit_button = None
            self.history_label = None
            self.history_content_list = None
            self.outline_frame = None

            self.history_window.destroy()
            self.history_window = None

    def change_language(self):
        """
        Change the language of the GUI elements based on the selected language.
        This method updates the text of labels, buttons, and other widgets
        to reflect the language change.

        """
        # Update text for labels
        for label in [self.settings_window, self.history_window, self.button_wrapper, self.frame_wrapper,
                      self.progress_wrapper, self.finished_window]:
            self.change_text(label)

        # Update text for buttons
        for button in [self.save_button, self.history_exit_button, self.browse_button, self.process_video_button,
                       self.media_player_button]:
            self.change_button_text(button)

        # Update image details if available
        if self.im_det is not None:
            self.im_det = "\n".join(
                [f"{self.lang[key]}: {self.image_detail_dict[key]}"
                 for key, value in self.image_detail_dict.items()])
        if self.image_details is not None:
            self.image_details.config(text=self.im_det)

        # Update result label with total difference
        if self.result_label is not None:
            self.result_label.config(
                text=f"{self.lang['diff']}: {processing.total_difference}")

    def change_button_text(self, button: custom_button.CustomButton):
        """
        Change the text of a custom button widget based on the selected language.

        :param button: The custom button widget whose text needs to be updated.
        :type button: custom_button.CustomButton
        """
        if button is not None and self.get_key(self.prev_lang_dict, button.get_text()) is not None:
            button.set_text(self.next_lang[self.get_key(self.prev_lang_dict, button.get_text())])

    def change_text(self, widget):
        """
        Change the text displayed on the widgets recursively within the given widget.

        :param widget: The parent widget whose children widgets' text needs to be updated.
        :type widget: tkinter.Widget or None
        """
        if widget is not None:
            # Update text for the parent widget
            if "text" in widget.keys():
                # Check if the current text has a translation available
                if self.get_key(self.prev_lang_dict, widget.cget("text")) in self.next_lang:
                    widget.config(text=self.next_lang[self.get_key(self.prev_lang_dict, widget.cget("text"))])

            # Recursively update text for children widgets
            for elem in widget.winfo_children():
                if "text" in elem.keys() and widget.winfo_children() is not None:
                    # Exclude specific widgets from text change
                    if elem not in [self.history_content_list, self.selected_file_path]:
                        # Check if the widget is not an OptionMenu or CustomButton
                        if not isinstance(elem, OptionMenu) and not isinstance(elem, custom_button.CustomButton):
                            # Check if the current text has a translation available
                            if self.get_key(self.prev_lang_dict, elem.cget("text")) in self.next_lang:
                                # Replace text with translated text
                                elem.config(text=elem.cget("text").replace(
                                    self.prev_lang_dict[self.get_key(self.prev_lang_dict, elem.cget("text"))],
                                    self.next_lang[self.get_key(self.prev_lang_dict, elem.cget("text"))]))
                                # Update UI to reflect changes
                                elem.update()
                                elem.update_idletasks()

    def get_key(self, my_dict: dict, value: str):
        for key, val in my_dict.items():
            if val == value:
                return key
        return None

    def update_colors(self):
        """
        Update the colors of the GUI elements to match the current theme settings.
        This method sets the background and foreground colors of various widgets,
        including the main window, history window, outline frame, and history content list.

        """
        # Set color for main window and history window
        self.set_color()
        self.change_colors(self.win)
        self.change_colors(self.history_window)

        # Set background color for outline frame if available
        if self.outline_frame is not None:
            self.outline_frame.config(bg=DARKER_BG)

        # Set colors for history content list items
        if self.history_content_list is not None and len(self.history_content_list) > 0:
            for elem in self.history_content_list:
                if elem is not None:
                    elem.config(fg=FONT_COLOR, bg=DARKER_BG)

        # Set background color for the main window
        self.win["bg"] = BGCOLOR

    def change_colors(self, widget):
        """
        Recursively update the background and foreground colors of the given widget
        and its children widgets to match the current theme settings.

        :param widget: The parent widget whose colors need to be updated.
        :type widget: tkinter.Widget or None
        """
        if widget is not None:
            # Update colors for the current widget
            for elem in widget.winfo_children():
                if elem is not None:
                    # Set background color if available
                    if "bg" in elem.keys():
                        elem.config(bg=BGCOLOR)
                    # Set foreground color if available
                    if "fg" in elem.keys():
                        elem.config(fg=FONT_COLOR)
                    # Recursively update colors for children widgets
                    if elem.winfo_children():
                        self.change_colors(elem)
