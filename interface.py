import os.path
import sys
import threading
import tkinter
from tkinter import Tk, Label, StringVar, filedialog, Toplevel, OptionMenu, Scrollbar, Canvas, \
    Frame
from tkcolorpicker import askcolor
import cv2

from PIL import Image, ImageTk

import config
import custom_ui

import debug

import custom_button
import history_handler
import lang
import prepass
import user_theme_config
import video_stabilization
import processing
import vlc_handler

# Global properties
LIGHT_BG = "#e8e8e8"
LIGHT_ACCENT = "#fafafa"
LIGHT_FONT_COLOR = "#000000"

DARK_BG = "#262626"
DARK_ACCENT = "#545454"
DARK_FONT_COLOR = "#ffffff"

PALENIGHT_BG = "#202331"
PALENIGHT_ACCENT = "#303754"
PALENIGHT_PB = "#78408f"

CHERRY_WHITE_BG = "#990011"
CHERRY_WHITE_ACCENT = "#fcebd4"
CHERRY_WHITE_PB = CHERRY_WHITE_BG

DARK_ORANGE_BG = "#46211A"
DARK_ORANGE_ACCENT = "#A43820"
DARK_ORANGE_PB = DARK_ORANGE_BG

u_t = user_theme_config.load_theme()
USER_BG = u_t["bg"]
USER_ACCENT = u_t["accent"]
USER_FONT_COLOR = u_t["text"]

BAR_BG_ACCENT = "#6AB187"
BASIC_PB_COLOR = "#73ff7b"
BGCOLOR = "#262626"
DARKER_BG = "#292929"
WHITE = "#ffffff"
BLACK = "#000000"
ACCENT = "#545454"
PB_COLOR = "#73ff7b"

DARK = "#262626"

FONT_COLOR = "#ffffff"
TIME_FONT_SIZE = 12
BIG_FONT_SIZE = 14
# FONT = ("Helvetica", TIME_FONT_SIZE)
# BOLD_FONT = ("Helvetica", TIME_FONT_SIZE, "bold")
FONT = ("Ubuntu", TIME_FONT_SIZE)
JET_FONT = ("JetBrains Mono", TIME_FONT_SIZE - 3)
BOLD_FONT = ("Ubuntu", TIME_FONT_SIZE, "bold")
BIG_FONT = ("Ubuntu", BIG_FONT_SIZE)
BIG_FONT_BOLD = ("Ubuntu", BIG_FONT_SIZE, "bold")

TIME_WRAPPER_WIDTH = 100
TIME_WRAPPER_HEIGHT = 80
WIN_WIDTH = 1300
WIN_HEIGHT = 590
FIN_WIN_WIDTH = 300
FIN_WIN_HEIGHT = 180
SET_WIN_WIDTH = 500
SET_WIN_HEIGHT = 500
HIS_WIN_WIDTH = 800
HIS_WIN_HEIGHT = 800

LOG_STATE = "On"

call_nr = 0
video_file_path = None
prev_video_path = None

manual_scroll = False
scroll_threshold = 0.96


class Interface:
    def __init__(self):
        self.clear_history_button = None
        self.clear_video_button = None
        self.apply_user_theme_button = None
        self.cards_list = None
        self.history_entries = None
        self.history_scroll_canvas = None
        self.history_scrollbar = None
        self.history_frame = None
        self.log_label_text = None
        self.log_canvas = None
        self.log_scrollbar = None
        self.log_frame = None
        self.log_text = None
        self.empty_label = None
        self.color_picker_items_squares = None
        self.color_picker_text_items = None
        self.color_picker_items = None
        self.user_theme_button = None
        self.log_label = None
        self.log_option_menu = None
        self.log_options = None
        self.terminal_wrapper = None
        self.terminal_text = None
        self.prepass_toggle_button = None
        self.stab_toggle_button = None
        self.periodic_exec_id = None
        self.terminate_program = False
        self.prep_pbar_overlay = None
        self.prep_wrapper = None
        self.prep_progress_bar = None
        self.prep_progress_label = None
        self.stab_pbar_overlay = None
        self.stab_progress_label = None
        self.stab_progress_bar = None
        self.stab_progress_wrapper = None
        self.proc_pbar_overlay = None
        self.proc_progress_bar = None
        self.history_title_frame = None
        self.settings_window_opened = False
        self.history_window_opened = False
        self.history_outline_frame = None
        self.theme_options = None
        self.theme_selected_option = None
        self.lang_option_menu = None
        self.theme_option_menu = None
        self.buttons_wrapper = None
        self.proc_progress_wrapper = None
        self.frame_wrapper = None
        self.next_lang = None
        self.previous_language = None
        self.prev_lang_dict = None
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
        self.settings_label = None
        self.settings_window = None
        self.proc_progress_wrapper = None
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
        self.win: tkinter.Tk
        self.time_label = None
        self.time_wrapper = None
        self.progress_bar = None
        self.proc_progress_label = None
        self.process_video_button = None
        self.browse_button = None
        self.is_file_selected = False
        self.opened_file_label = None
        self.settings_button = None
        self.settings = config.load_settings()
        self.curr_lang = self.settings[0]
        self.curr_theme = self.settings[1]
        self.log_state = self.settings[2]
        self.image_detail_dict = None
        self.browse_wrapper = None
        self.browse_button = None

        self.set_color()

        debug.log("[Interface] [1/1] Creating interface...", text_color="blue")

        self.lang = lang.load_lang(self.curr_lang)

        self.set_properties()
        self.create_buttons_wrapper()
        self.create_settings_button()
        self.create_history_button()
        self.create_browser()

        self.create_terminal()

        debug.log("[Interface] [1/2] Interface created", text_color="blue")
        self.set_interface()
        self.win.mainloop()

    def set_interface(self):
        custom_ui.set_interface_instance(self)

    def set_main_focus(self):
        self.win.focus_set()

    def set_log_text(self):
        global manual_scroll
        new_text = ""
        curr_text = self.log_text.get()

        with open(debug.log_file_path, 'r') as log_file:
            for line in log_file:
                new_text += line[32:]

        if curr_text in new_text:
            index = new_text.find(curr_text) + len(curr_text)
            new_text = new_text[index:]
        else:
            new_text = new_text
            print(new_text)

        self.log_text.set(curr_text + new_text)

        self.log_frame.update_idletasks()
        self.log_canvas.config(scrollregion=self.log_canvas.bbox("all"))

        if not manual_scroll:
            self.log_canvas.yview_moveto(1.0)

        if float(self.log_canvas.yview()[1]) >= scroll_threshold:
            self.log_canvas.yview_moveto(1.0)

    def create_terminal(self):
        self.terminal_wrapper = custom_ui.CustomLabelFrame(self.win,
                                                           text="Log",
                                                           width=490,
                                                           height=WIN_HEIGHT - 20,
                                                           radius=15,
                                                           fill=ACCENT,
                                                           fg=FONT_COLOR,
                                                           bg=BGCOLOR)
        self.terminal_wrapper.canvas.place(x=800, y=10)

        self.empty_label = Label(self.terminal_wrapper.canvas, width=1, height=1, bg=ACCENT, borderwidth=0)
        self.empty_label.place(x=10, y=30)

        self.log_canvas = Canvas(self.empty_label, width=470, height=WIN_HEIGHT - 75, bg=ACCENT, highlightthickness=0)

        self.log_scrollbar = Scrollbar(self.empty_label, orient="vertical", command=self.log_canvas.yview, width=5)
        self.log_scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_scrollbar.grid_forget()

        self.log_canvas.config(yscrollcommand=self.log_scrollbar.set)
        self.log_canvas.grid(row=0, column=0, sticky="nsew")

        self.log_frame = Frame(self.log_canvas, bg=ACCENT)
        self.log_canvas.create_window((0, 0), window=self.log_frame, anchor="nw")

        self.log_text = StringVar()
        self.log_label_text = Label(self.log_frame, textvariable=self.log_text, bg=ACCENT, fg=FONT_COLOR,
                                    wraplength=468, justify="left",
                                    font=JET_FONT)
        self.log_label_text.pack()

        self.log_scrollbar.bind("<MouseWheel>", self.on_mousewheel_log)
        self.log_label_text.bind("<MouseWheel>", self.on_mousewheel_log)
        self.log_canvas.bind("<MouseWheel>", self.on_mousewheel_log)

        self.log_frame.update_idletasks()

    def set_scroll_to_bottom(self):
        self.log_canvas.yview_moveto(1.0)

    def on_mousewheel_log(self, event):
        global manual_scroll
        # Set manual_scroll to True when the user manually scrolls
        manual_scroll = True

        if event.num == 5 or event.delta == -120:
            if self.log_canvas.yview()[1] < 1.0:
                self.log_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            if self.log_canvas.yview()[0] > 0.0:
                self.log_canvas.yview_scroll(-1, "units")

    def set_color(self):
        """
        Sets global color variables based on the current theme.

        This function updates the global variables BGCOLOR, FONT_COLOR, ACCENT, and PB_COLOR
        based on the current theme specified in `self.curr_theme`.

        Global Variables:
            BGCOLOR (str): Background color.
            FONT_COLOR (str): Font color.
            ACCENT (str): Accent color.
            PB_COLOR (str): Progress bar color.
        """
        global BGCOLOR, FONT_COLOR, ACCENT, PB_COLOR

        # Dictionary mapping theme names to corresponding color tuples
        theme_colors = {
            "dark": (DARK_BG, DARK_FONT_COLOR, DARK_ACCENT, BASIC_PB_COLOR),
            "light": (LIGHT_BG, LIGHT_FONT_COLOR, LIGHT_ACCENT, BASIC_PB_COLOR),
            "palenight": (PALENIGHT_BG, DARK_FONT_COLOR, PALENIGHT_ACCENT, BASIC_PB_COLOR),
            "cherrywhite": (CHERRY_WHITE_BG, LIGHT_FONT_COLOR, CHERRY_WHITE_ACCENT, BASIC_PB_COLOR),
            "brownorange": (DARK_ORANGE_BG, DARK_FONT_COLOR, DARK_ORANGE_ACCENT, BASIC_PB_COLOR),
            "usertheme": (USER_BG, USER_FONT_COLOR, USER_ACCENT, BASIC_PB_COLOR)
        }

        # Set global color variables based on the current theme
        if self.curr_theme in theme_colors:
            BGCOLOR, FONT_COLOR, ACCENT, PB_COLOR = theme_colors[self.curr_theme]

    def toggle_log(self, to_state):
        if to_state == "On":
            self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
            self.log_state = "On"
        if to_state == "Off":
            self.win.geometry("800x" + str(WIN_HEIGHT))
            self.log_state = "Off"

    def set_properties(self):
        # Set windows properties
        debug.log("[Interface] [2/1] Setting properties...", text_color="magenta")

        self.win = Tk()
        self.win["bg"] = BGCOLOR
        self.win.title(self.lang["title"])
        if self.log_state == "On":
            self.win.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        else:
            self.win.geometry("800x" + str(WIN_HEIGHT))
        self.win.resizable(False, False)
        # self.win.protocol(self.on_window_close)
        self.win.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.selected_file_path = StringVar()
        # self.create_font()
        debug.log("[Interface] [2/2] Properties set!\n", text_color="magenta")

        self.win.after(150, self.schedule_periodic_processing_execution)
        self.win.after(150, self.schedule_terminal_update)

    def schedule_terminal_update(self):
        # self.update_terminal_text()
        self.set_log_text()
        if float(self.log_canvas.yview()[1]) > scroll_threshold:
            self.log_canvas.yview_moveto(1.0)
        self.win.after(150, self.schedule_terminal_update)

    def schedule_periodic_processing_execution(self):
        if processing.initialized and processing.callback_queue.qsize() > 0:
            processing.execute_callbacks()

        self.periodic_exec_id = self.win.after(150, self.schedule_periodic_processing_execution)
        if processing.is_finished:
            processing.execute_callbacks()
            self.stop_periodic_progress_update()
            processing.video_writer.release()
            processing.thread.join()
            self.create_finished_window()

    def stop_periodic_progress_update(self):
        if self.periodic_exec_id is not None:
            self.win.after_cancel(self.periodic_exec_id)
            self.periodic_exec_id = None
            # self.create_finished_window()

    def on_window_close(self):
        # self.terminate_program = True
        # prepass.stop_thread = True
        # prepass.thread.join()
        # prepass.is_finished = True
        # prepass.thread = None
        #
        # video_stabilization.stop_thread = True
        # video_stabilization.thread.join()
        # video_stabilization.is_finished = True
        # video_stabilization.thread = None
        # processing.stop_thread = True
        # processing.thread.join()

        debug.log("[Interface] Stopping all threads!!!")
        self.stop_periodic_progress_update()
        debug.log("[Interface] Stopping prepass thread...", text_color="yellow")
        prepass.stop_prepass_thread()
        debug.log("[Interface] Stopped prepass thread!", text_color="magenta")

        debug.log("[Interface] Stopping stabilization thread...", text_color="yellow")
        video_stabilization.stop_stabilization_thread()
        debug.log("[Interface] Stopped stabilization thread!", text_color="magenta")

        processing.force_terminate = True
        processing.stop_processing_thread()
        debug.log("[Interface] Stopped threads")
        self.win.destroy()
        sys.exit(2)

    def create_buttons_wrapper(self):
        # Create wrapper for settings and history buttons
        self.buttons_wrapper = custom_ui.CustomLabelFrame(self.win, text="",
                                                          fill=ACCENT,
                                                          fg=FONT_COLOR,
                                                          bg=BGCOLOR,
                                                          width=150,
                                                          height=80,
                                                          radius=15)
        self.buttons_wrapper.canvas.place(x=10, y=10)

    def create_settings_button(self):
        # Create button to open settings window
        self.settings_button = custom_button.CustomButton(self.buttons_wrapper.canvas,
                                                          command=self.create_settings_window,
                                                          button_type=custom_button.settings_button,
                                                          bg=ACCENT)
        self.settings_button.canvas.place(x=10, y=self.buttons_wrapper.get_height() // 8)

    def create_history_button(self):
        # Create button to open window containing processing history
        self.history_button = custom_button.CustomButton(self.buttons_wrapper.canvas,
                                                         command=lambda: self.create_history_window(),
                                                         button_type=custom_button.history_button,
                                                         bg=ACCENT)
        self.history_button.canvas.place(x=80, y=self.buttons_wrapper.get_height() // 8)

    def run_browser_on_thread(self):
        # Run the file browser on a separate thread
        file_browser_thread = threading.Thread(target=self.create_browser)
        file_browser_thread.start()

    def create_browser(self):
        # Wrapper for file browsing
        debug.log("[Interface] [4/1] Creating Browsing wrapper...", text_color="magenta")
        self.browse_wrapper = custom_ui.CustomLabelFrame(self.win,
                                                         text=self.lang["input_file"],
                                                         fill=ACCENT,
                                                         fg=FONT_COLOR,
                                                         bg=BGCOLOR,
                                                         width=620,
                                                         height=80,
                                                         radius=15)
        self.browse_wrapper.canvas.place(x=170, y=10)
        debug.log("[Interface] [4/2] Browsing wrapper created!", text_color="magenta")

        debug.log("[Interface] [4/3] Creating browse Button...", text_color="magenta")
        self.browse_button = custom_button.CustomButton(self.browse_wrapper.canvas,
                                                        text=self.lang["browse"],
                                                        command=self.browse_files,
                                                        bg=ACCENT,
                                                        button_type=custom_button.button)
        self.browse_button.canvas.place(x=10, y=30)

        debug.log("[Interface] [4/4] Browse Button created!", text_color="magenta")

        # Label for showing opened file path
        debug.log("[Interface] [4/5] Creating file path Label...", text_color="magenta")
        self.opened_file_label = Label(self.browse_wrapper.canvas,
                                       textvariable=self.selected_file_path,
                                       fg=FONT_COLOR,
                                       bg=ACCENT,
                                       font=FONT,
                                       wraplength=520,
                                       justify="left")
        self.opened_file_label.config(text=self.lang["None"], anchor="center")

        # Place right to the button, vertically centered
        self.opened_file_label.place(x=85, y=self.browse_button.winfo_reqheight())
        debug.log("[Interface] [4/6] File path Label created!\n", text_color="magenta")

    def set_selected_file_path(self, path):
        if os.path.exists(path):
            global video_file_path, prev_video_path
            self.selected_file_path.set(path)
            self.show_first_frame_details(path)
            video_file_path = path
            prev_video_path = video_file_path
        else:
            debug.log("[Interface] [-] File path does not exist!", text_color="red")

    def browse_files(self):
        # Open a file dialog and get the selected file path
        global video_file_path
        global prev_video_path
        video_file_path = prev_video_path
        debug.log("[Interface] Opening file browser dialog...", text_color="magenta")
        file_path = filedialog.askopenfilename(title="Select a file",
                                               filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv")])

        # Update the label with the selected file path
        if file_path:
            # self.selected_file_path.set(file_path)
            self.set_selected_file_path(file_path)
            debug.log(f"[Interface] Selected file: {file_path}", text_color="blue")
            self.show_first_frame_details(file_path)
            video_file_path = file_path
            prev_video_path = video_file_path
        else:
            debug.log("[Interface] No file selected", text_color="red")
            if prev_video_path:
                debug.log("[Interface] Selecting previous video", text_color="blue")
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
        debug.log("[Interface] [5/1] Creating video details wrapper...", text_color="yellow")
        self.frame_wrapper = custom_ui.CustomLabelFrame(self.win,
                                                        text=self.lang["video_data"],
                                                        fill=ACCENT,
                                                        fg=FONT_COLOR,
                                                        bg=BGCOLOR,
                                                        radius=15,
                                                        width=780,
                                                        height=320)
        self.frame_wrapper.canvas.place(x=10, y=100)
        debug.log("[Interface] [5/2] Video details wrapper created!", text_color="yellow")

        # Creating a label to display the first frame of the video
        debug.log("[Interface] [5/3] Creating placeholder label for first frame...", text_color="yellow")
        frame_label = Label(self.frame_wrapper.canvas)
        frame_label.place(x=10, y=self.frame_wrapper.get_label_height() + 10)
        debug.log("[Interface] [5/4] First frame placeholder created!", text_color="yellow")

        # Opening the video and extracting details from the first frame
        debug.log("[Interface] [5/5] Opening video and getting first frame data...", text_color="yellow")

        cap = cv2.VideoCapture(path)
        fps = "{:.0f}".format(cap.get(cv2.CAP_PROP_FPS))
        bitrate = "{:.0f}".format(cap.get(cv2.CAP_PROP_BITRATE))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = "{:.0f}s".format(frame_count / int(fps))

        ret, frame = cap.read()
        cap.release()
        debug.log("[Interface] [5/6] First frame data gathered!", text_color="yellow")

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
            debug.log("[Interface] [5/7] Calculating first frame information...", text_color="yellow")
            new_width = self.frame_wrapper.get_width() // 2
            new_height = int(new_width / aspect_ratio)
            image = image.resize((new_width, new_height), Image.BILINEAR)
            image_file = ImageTk.PhotoImage(image)
            debug.log("[Interface] [5/8] First image information set!", text_color="yellow")

            # Configuring the frame label with the resized first frame
            debug.log("[Interface] [5/9] Configuring image...", text_color="yellow")
            frame_label.config(image=image_file)
            frame_label.image = image_file
            debug.log("[Interface] [5/10] Image configured!", text_color="yellow")

        # Creating button to open the video with VLC
        self.media_player_button = custom_button.CustomButton(self.frame_wrapper.canvas,
                                                              text=self.lang["open_vlc"],
                                                              bg=ACCENT,
                                                              width=110,
                                                              height=30,
                                                              # command=lambda: self.open_media_player(path))
                                                              command=lambda: vlc_handler.open_video(path))
        self.media_player_button.canvas.place(x=10,
                                              y=new_height + 40)

        # Creating button to start processing
        self.process_video_button = custom_button.CustomButton(self.frame_wrapper.canvas,
                                                               text=self.lang["process"],
                                                               bg=ACCENT,
                                                               width=110,
                                                               height=30,
                                                               command=lambda: self.process_video())
        self.process_video_button.canvas.place(x=self.media_player_button.winfo_reqwidth() + 20, y=new_height + 40)

        # Creating labels to display video details
        debug.log("[Interface] [5/11] Creating labels to display video details...", text_color="yellow")
        self.frame_details_header = Label(self.frame_wrapper.canvas,
                                          text=self.lang["video_det"],
                                          fg=FONT_COLOR,
                                          bg=ACCENT,
                                          font=BIG_FONT_BOLD)
        self.frame_details_header.place(x=new_width + 30, y=20)
        self.image_details = Label(self.frame_wrapper.canvas,
                                   text=self.im_det,
                                   fg=FONT_COLOR,
                                   bg=ACCENT,
                                   font=FONT,
                                   # Left alignment
                                   justify="left",
                                   anchor="w"
                                   )
        self.image_details.place(x=new_width + 30,
                                 y=self.frame_details_header.winfo_y() + self.frame_details_header.winfo_reqheight() + 20)
        debug.log("[Interface] [5/12] Labels to display video details created!\n", text_color="yellow")
        if self.log_canvas is not None:
            self.log_canvas.yview_moveto(1.0)

        self.prepass_toggle_button = custom_ui.CustomToggleButton(self.frame_wrapper.canvas,
                                                                  text=self.lang["normalization"],
                                                                  width=60,
                                                                  height=30,
                                                                  bg=ACCENT)
        self.prepass_toggle_button.canvas.place(x=new_width + 30, y=190)

        self.stab_toggle_button = custom_ui.CustomToggleButton(self.frame_wrapper.canvas,
                                                               text=self.lang["stabilization"],
                                                               width=60,
                                                               height=30,
                                                               bg=ACCENT)
        self.stab_toggle_button.canvas.place(x=new_width + 30, y=230)

        self.plotting_toggle_button = custom_ui.CustomToggleButton(self.frame_wrapper.canvas,
                                                                   text=self.lang["to_plot"],
                                                                   width=60,
                                                                   height=30,
                                                                   state=False,
                                                                   bg=ACCENT)
        self.plotting_toggle_button.canvas.place(x=new_width + 30, y=270)

    def process_video(self):
        """
        Initiates the video processing task.

        Disables relevant buttons, creates a progress bar, sets the progress callback,
        and starts a separate thread for video processing.
        """
        if video_file_path:
            # Disable buttons to prevent multiple processing requests
            self.process_video_button.disable()
            self.browse_button.disable()
            self.prepass_toggle_button.disable()
            self.stab_toggle_button.disable()
            self.plotting_toggle_button.disable()

            # Create and display a progress bar
            # self.create_preprocess_progress_bar()
            self.create_stabilization_progress_bar()
            self.create_processing_progress_bar()

            # Set the progress callback functions
            # processing.set_progress_callback(self.update_bar)
            # opencv_stabilization.set_progress_callback(self.update_bar)
            # video_stabilization.set_progress_callback(self.update_bar)
            # prepass.set_progress_callback(self.update_bar)

            # Start video processing in a separate thread
            self.win.after(150, self.schedule_periodic_processing_execution)
            debug.log(f"[Interface] Preprocessing: {self.prepass_toggle_button.get_state()}")
            debug.log(f"[Interface] Stabilization: {self.stab_toggle_button.get_state()}")
            debug.log(f"[Interface] Plotting: {self.plotting_toggle_button.get_state()}\n")

            processing.process_video_thread(video_file_path,
                                            self.prepass_toggle_button.get_state(),
                                            self.stab_toggle_button.get_state(),
                                            self.plotting_toggle_button.get_state(),
                                            self.update_bar)
            self.set_scroll_to_bottom()

    def create_preprocess_progress_bar(self):
        self.prep_wrapper = custom_ui.CustomLabelFrame(self.win,
                                                       text=self.lang["preprocessing"],
                                                       width=780,
                                                       height=70,
                                                       fill=ACCENT,
                                                       fg=FONT_COLOR,
                                                       radius=15,
                                                       bg=BGCOLOR)
        self.prep_wrapper.canvas.place(x=10, y=430)

        self.prep_progress_bar = custom_ui.CustomProgressBar(self.prep_wrapper.canvas,
                                                             width=705,
                                                             height=30,
                                                             padding=6,
                                                             bg=ACCENT,
                                                             bar_bg_accent=BAR_BG_ACCENT,
                                                             pr_bar=PB_COLOR)

        self.prep_progress_bar.canvas.place(x=10, y=self.prep_wrapper.get_height() // 2 - 5)

        self.prep_progress_label = Label(self.prep_wrapper.canvas,
                                         text="0%",
                                         fg=FONT_COLOR,
                                         bg=ACCENT,
                                         font=BOLD_FONT)
        self.prep_progress_label.place(x=720, y=30)

        self.prep_pbar_overlay = custom_ui.CustomLabelFrame(self.prep_wrapper.canvas, width=690, height=30,
                                                            bg=ACCENT, fill=ACCENT)
        self.prep_pbar_overlay.canvas.place(x=20, y=self.prep_progress_bar.get_height() * 2)

    def create_stabilization_progress_bar(self):
        self.stab_progress_wrapper = custom_ui.CustomLabelFrame(self.win,
                                                                text=self.lang["preprocessing"],
                                                                width=780,
                                                                height=70,
                                                                fill=ACCENT,
                                                                fg=FONT_COLOR,
                                                                radius=15,
                                                                bg=BGCOLOR)
        self.stab_progress_wrapper.canvas.place(x=10, y=430)

        self.stab_progress_bar = custom_ui.CustomProgressBar(self.stab_progress_wrapper.canvas,
                                                             width=705,
                                                             height=30,
                                                             padding=6,
                                                             bg=ACCENT,
                                                             bar_bg_accent=BAR_BG_ACCENT,
                                                             pr_bar=PB_COLOR)
        self.stab_progress_bar.canvas.place(x=10, y=self.stab_progress_wrapper.get_height() // 2 - 5)

        self.stab_progress_label = Label(self.stab_progress_wrapper.canvas, text="0%", fg=FONT_COLOR, bg=ACCENT,
                                         font=BOLD_FONT)
        self.stab_progress_label.place(x=720, y=30)
        debug.log("[Interface] [6/6] Progress label created!", text_color="magenta")

        # Create an overlay frame for the progress bar to hide flickering bug
        self.stab_pbar_overlay = custom_ui.CustomLabelFrame(self.stab_progress_wrapper.canvas, width=690, height=30,
                                                            bg=ACCENT, fill=ACCENT)
        self.stab_pbar_overlay.canvas.place(x=20, y=self.stab_progress_bar.get_height() * 2)

    def create_processing_progress_bar(self):
        """
        Creates and displays a custom progress bar with a progress label.
        """
        debug.log("[Interface] [6/1] Creating progress wrapper...", text_color="magenta")
        # Create a wrapper frame for the progress bar
        self.proc_progress_wrapper = custom_ui.CustomLabelFrame(self.win,
                                                                text=self.lang["progress"],
                                                                width=780,
                                                                height=70,
                                                                fill=ACCENT,
                                                                fg=FONT_COLOR,
                                                                radius=15,
                                                                bg=BGCOLOR)
        self.proc_progress_wrapper.canvas.place(x=10, y=510)
        debug.log("[Interface] [6/2] Progress wrapper created!", text_color="magenta")

        # Create the custom progress bar
        debug.log("[Interface] [6/3] Creating custom progress bar...", text_color="magenta")
        self.proc_progress_bar = custom_ui.CustomProgressBar(self.proc_progress_wrapper.canvas,
                                                             width=705,
                                                             height=30,
                                                             padding=6,
                                                             bg=ACCENT,
                                                             bar_bg_accent=BAR_BG_ACCENT,
                                                             pr_bar=PB_COLOR)
        self.proc_progress_bar.canvas.place(x=10, y=self.proc_progress_wrapper.get_height() // 2 - 5)
        debug.log("[Interface] [6/4] Custom progress bar created!", text_color="magenta")

        # Create and place the progress label
        debug.log("[Interface] [6/5] Creating progress label...", text_color="magenta")
        self.proc_progress_label = Label(self.proc_progress_wrapper.canvas, text="0%", fg=FONT_COLOR, bg=ACCENT,
                                         font=BOLD_FONT)
        self.proc_progress_label.place(x=720, y=30)
        debug.log("[Interface] [6/6] Progress label created!\n", text_color="magenta")
        if self.log_canvas is not None:
            self.log_canvas.yview_moveto(1.0)

        # Create an overlay frame for the progress bar to hide flickering bug
        self.proc_pbar_overlay = custom_ui.CustomLabelFrame(self.proc_progress_wrapper.canvas, width=690, height=30,
                                                            bg=ACCENT, fill=ACCENT)
        self.proc_pbar_overlay.canvas.place(x=20, y=self.proc_progress_bar.get_height() * 2)

    def update_bar(self, bar: str, value: int):
        if bar == "preprocessing":
            self.prep_progress_bar.set_percentage(value)
            self.prep_progress_label['text'] = f"{value} %"
        elif bar == "stabilization":
            self.stab_progress_bar.set_percentage(value)
            self.stab_progress_label['text'] = f"{value} %"
        elif bar == "processing":
            self.proc_progress_bar.set_percentage(value)
            self.proc_progress_label['text'] = f"{value} %"

    def update_progress(self, value: int):
        """
        Updates the progress bar and label with the given value.

        Parameters:
            value (int): The progress value to be displayed.
        """
        # Set the progress bar percentage
        self.proc_progress_bar.set_percentage(value)

        # Update the progress label with the current value
        self.proc_progress_label['text'] = f"{value} %"

        # Check if processing has finished
        if processing.finished:
            # Log the processing difference in the debug console
            debug.log(f"[Interface] {self.lang['diff']}: {processing.total_difference}", text_color="blue")

            # Create and display the finished window
            # self.create_finished_window()

    def create_finished_window(self):
        """
        Creates and displays the window to show processing result.

        If the window already exists, it will be closed before creating a new one.
        """
        # Close existing finished window if it exists
        if self.finished_window is not None:
            self.close_finished_windows(to_debug=False)

        # Create a new Toplevel window for displaying processing result
        self.finished_window = Toplevel(self.win)
        self.finished_window.title(self.lang["result_win_title"])
        self.finished_window.geometry(str(FIN_WIN_WIDTH) + "x" + str(FIN_WIN_HEIGHT))
        self.finished_window.configure(background=ACCENT)
        self.finished_window.resizable(False, False)
        debug.log(f"[Interface] Finished window opened!")

        # Center the finished window on the screen
        screen_width = self.finished_window.winfo_screenwidth()
        screen_height = self.finished_window.winfo_screenheight()
        x = (screen_width - FIN_WIN_WIDTH) // 2
        y = (screen_height - FIN_WIN_HEIGHT) // 2
        self.finished_window.geometry(f"+{x}+{y}")

        # Add labels and buttons to the finished window
        self.finished_title_label = Label(self.finished_window,
                                          text=self.lang["proc_finished"],
                                          fg=FONT_COLOR,
                                          bg=ACCENT,
                                          font=BOLD_FONT)
        self.finished_title_label.pack(pady=20)

        self.result_label = Label(self.finished_window,
                                  text=f"{self.lang['diff']}: {processing.get_result()}",
                                  fg=FONT_COLOR,
                                  bg=ACCENT,
                                  font=FONT)
        self.result_label.pack(pady=0)

        self.ok_button = custom_button.CustomButton(self.finished_window,
                                                    text=self.lang["ok"],
                                                    bg=ACCENT,
                                                    command=self.close_finished_windows,
                                                    button_type=custom_button.button)
        self.ok_button.canvas.pack(pady=20)

        # Enable buttons in the main window
        self.process_video_button.enable()
        self.browse_button.enable()
        self.prepass_toggle_button.enable()
        self.stab_toggle_button.enable()
        self.plotting_toggle_button.enable()

    def close_finished_windows(self, to_debug=True):
        self.browse_button.enable()
        self.process_video_button.enable()
        self.ok_button.destroy()
        self.finished_window.destroy()
        if to_debug:
            debug.log("[Interface] Finished window closed!", text_color="cyan")

    def create_settings_window(self):
        """
        Creates the settings window.

        This method creates a window where users can configure settings such as language and theme.

        Args:
            self: The instance of the Interface class.

        Returns:
            None
        """
        if self.settings_window_opened is True:
            self.settings_window.focus_set()
            return

        # Create the settings window
        self.settings_window = Toplevel(self.win)
        self.settings_window.title(self.lang["settings"])
        self.settings_window.geometry(f"{SET_WIN_WIDTH}x{SET_WIN_HEIGHT}")
        self.settings_window.configure(background=BGCOLOR)
        self.settings_window.resizable(False, False)
        self.settings_window.bind("<Destroy>", lambda e: self.close_settings_window())

        # Add a label for the settings window title
        self.settings_wrapper = custom_ui.CustomLabelFrame(self.settings_window,
                                                           width=SET_WIN_WIDTH - 20,
                                                           height=SET_WIN_HEIGHT - 20,
                                                           fg=FONT_COLOR,
                                                           radius=15,
                                                           fill=ACCENT,
                                                           bg=BGCOLOR)
        self.settings_wrapper.canvas.place(x=10, y=10)
        self.settings_label = Label(self.settings_wrapper.canvas,
                                    text=self.lang["settings"],
                                    fg=FONT_COLOR,
                                    bg=ACCENT,
                                    font=BOLD_FONT,
                                    anchor="center")
        self.settings_label.place(x=self.settings_wrapper.get_width() // 2 - self.settings_label.winfo_reqwidth() // 2,
                                  y=10)

        # Add a label for the language selection
        self.lang_label = Label(self.settings_wrapper.canvas,
                                text=self.lang["lang"],
                                fg=FONT_COLOR,
                                bg=ACCENT,
                                font=FONT, )
        self.lang_label.place(x=(self.settings_wrapper.get_width() - self.lang_label.winfo_reqwidth()) // 2 - 40,
                              y=self.settings_label.winfo_y() + 50)

        # Define language options
        self.lang_options = [self.lang["english"], self.lang["hungarian"]]

        # Set default language option based on current language setting
        self.lang_selected_option = StringVar(self.settings_window)
        self.lang_selected_option.set(self.lang_options[1] if self.curr_lang == "hungarian" else self.lang_options[0])

        # Add language OptionMenu
        self.lang_option_menu = OptionMenu(self.settings_wrapper.canvas, self.lang_selected_option, *self.lang_options)
        self.lang_option_menu.config(anchor="center",
                                     bg=ACCENT,
                                     fg=FONT_COLOR,
                                     activebackground=ACCENT,
                                     # activeforeground=FONT_COLOR,
                                     highlightbackground=ACCENT)
        self.lang_option_menu.place(x=(self.settings_wrapper.get_width() - self.lang_label.winfo_reqwidth()) // 2 + 40,
                                    y=self.lang_label.winfo_reqheight() * 2)

        # Add a label for the theme selection
        self.theme_label = Label(self.settings_wrapper.canvas,
                                 text=self.lang["theme"],
                                 fg=FONT_COLOR,
                                 bg=ACCENT,
                                 font=FONT,
                                 anchor="center")
        self.theme_label.place(x=(self.settings_wrapper.get_width() - self.lang_label.winfo_reqwidth()) // 2 - 40,
                               y=self.lang_label.winfo_reqheight() * 4)

        # Define theme options
        self.theme_options = [self.lang["dark"], self.lang["light"], self.lang["palenight"], self.lang["cherrywhite"],
                              self.lang["brownorange"], self.lang["user_theme"]]

        # Set default theme option based on current theme setting
        self.theme_selected_option = StringVar(self.settings_wrapper.canvas)

        # Map theme index
        theme_index_mapping = {
            "dark": 0,
            "light": 1,
            "palenight": 2,
            "cherrywhite": 3,
            "brownorange": 4,
            "usertheme": 5
        }
        self.theme_selected_option.set(self.theme_options[theme_index_mapping.get(self.curr_theme, 0)])

        # Add theme OptionMenu
        self.theme_option_menu = OptionMenu(self.settings_wrapper.canvas, self.theme_selected_option,
                                            *self.theme_options)
        self.theme_option_menu.config(anchor="center",
                                      bg=ACCENT,
                                      fg=FONT_COLOR,
                                      activebackground=ACCENT,
                                      activeforeground=FONT_COLOR,
                                      highlightbackground=ACCENT)
        self.theme_option_menu.place(x=(self.settings_wrapper.get_width() - self.lang_label.winfo_reqwidth()) // 2 + 40,
                                     y=self.lang_label.winfo_reqheight() * 4)

        self.log_label = Label(self.settings_wrapper.canvas,
                               text="Log",
                               fg=FONT_COLOR,
                               bg=ACCENT,
                               font=FONT,
                               anchor="center")
        self.log_label.place(x=(self.settings_wrapper.get_width() - self.lang_label.winfo_reqwidth()) // 2 - 40,
                             y=self.lang_label.winfo_reqheight() * 6)

        self.log_options = ["On", "Off"]
        selected_log_option = StringVar(self.settings_wrapper.canvas)
        if self.log_state == "On":
            selected_log_option.set(self.log_options[0])
        else:
            selected_log_option.set(self.log_options[1])
        self.log_option_menu = OptionMenu(self.settings_wrapper.canvas, selected_log_option, *self.log_options)
        self.log_option_menu.config(anchor="center",
                                    bg=ACCENT,
                                    fg=FONT_COLOR,
                                    activebackground=ACCENT,
                                    activeforeground=FONT_COLOR,
                                    highlightbackground=ACCENT)
        self.log_option_menu.place(x=(self.settings_wrapper.get_width() - self.lang_label.winfo_reqwidth()) // 2 + 40,
                                   y=self.lang_label.winfo_reqheight() * 6)

        self.settings_window_opened = True

        def save_option():
            """
            Saves the selected language and theme options.

            This function retrieves the selected language and theme options from the OptionMenu widgets
            and saves them to the configuration file. It also displays a message prompting the user to
            restart the program for the changes to take effect.
            """

            # Retrieve selected language and theme option
            chosen_lang_option = self.lang_selected_option.get()
            chosen_theme_option = self.theme_selected_option.get()
            chosen_log_state = selected_log_option.get()

            # Map language options to standard format
            chosen_lang_option = "hungarian" if chosen_lang_option in ("Magyar", "Hungarian") else "english"
            # Map theme options
            theme_options_mapping = {
                "Dark": "dark",
                "Light": "light",
                "Palenight": "palenight",
                "Cherry White": "cherrywhite",
                "Brown Orange": "brownorange",
                self.lang["user_theme"]: "usertheme"
            }
            chosen_theme_option = theme_options_mapping.get(chosen_theme_option, chosen_theme_option.lower())

            if chosen_lang_option != self.curr_lang:
                self.prev_lang_dict = lang.load_lang(self.curr_lang)
                self.next_lang = lang.load_lang(chosen_lang_option)

                self.lang = lang.load_lang(chosen_lang_option)
                self.curr_lang = chosen_lang_option
                self.change_language()

            if chosen_theme_option != self.curr_theme or chosen_theme_option == theme_options_mapping[
                self.lang["user_theme"]]:
                self.curr_theme = chosen_theme_option
                self.update_colors()
                if chosen_theme_option == theme_options_mapping[self.lang["user_theme"]]:
                    self.user_theme_button.canvas.place(x=360, y=self.lang_label.winfo_reqheight() * 4)
                else:
                    self.user_theme_button.canvas.place(x=1000, y=1000)

            # if chosen_theme_option == theme_options_mapping["User Theme"]:
            #     # self.user_theme_button.canvas.place(x=350, y=self.lang_label.winfo_reqheight() * 4)
            # else:
            #     # self.user_theme_button.canvas.place(x=200, y=200)

            if chosen_log_state != self.log_state:
                self.toggle_log(chosen_log_state)

            # Save selected options to configuration file
            debug.log(
                f"[Interface] Settings - Language: {chosen_lang_option}, Theme: {chosen_theme_option}, Log: {chosen_log_state}",
                text_color="yellow")
            config.save_settings([chosen_lang_option, chosen_theme_option, chosen_log_state])

        # Add a button to save the selected options
        self.save_button = custom_button.CustomButton(self.settings_wrapper.canvas,
                                                      text=self.lang["save"],
                                                      command=save_option,
                                                      button_type=custom_button.button,
                                                      bg=ACCENT)

        self.save_button.canvas.place(x=SET_WIN_WIDTH // 2 - self.save_button.winfo_reqwidth() // 2 - 10,
                                      y=200)
        self.user_theme_button = custom_button.CustomButton(self.settings_wrapper.canvas, text=self.lang["configure"],
                                                            bg=ACCENT,
                                                            command=self.show_color_configurer)

        self.clear_history_button = custom_button.CustomButton(self.settings_wrapper.canvas,
                                                               text=self.lang["clear_history"],
                                                               bg=ACCENT,
                                                               command=history_handler.clear_history)
        self.clear_history_button.canvas.place(
            x=SET_WIN_WIDTH // 2 - self.clear_history_button.winfo_reqwidth() // 2 - 10,
            y=280)

        self.clear_video_button = custom_button.CustomButton(self.settings_wrapper.canvas,
                                                             text=self.lang["clear_video"],
                                                             bg=ACCENT,
                                                             command=processing.clear_processed_videos)
        self.clear_video_button.canvas.place(
            x=SET_WIN_WIDTH // 2 - self.clear_video_button.winfo_reqwidth() // 2 - 10,
            y=320)

        if self.curr_theme == "usertheme":
            self.user_theme_button.canvas.place(x=360, y=self.lang_label.winfo_reqheight() * 4)
        else:
            self.user_theme_button.canvas.place(x=1000, y=1000)

    def apply_user_theme(self):
        self.update_colors()

    def show_color_configurer(self):
        def choose_color(lab, c_type):
            # Open the color picker dialog
            color = askcolor(title="Choose Color", parent=top)

            # If a color is selected, update the label's background color
            if color[1]:
                lab.config(bg=color[1])
                if c_type == "accent":
                    user_theme["accent"] = color[1]
                    self.clf.switch_theme(new_fill=color[1])
                    self.clf_button.config(bg=color[1])
                elif c_type == "bg":
                    user_theme["bg"] = color[1]
                    self.clf_canvas.config(bg=color[1])
                    self.clf.switch_theme(new_bg=color[1])
                elif c_type == "text":
                    user_theme["text"] = color[1]
                    self.clf.switch_theme(new_text_color=color[1])

                user_theme_config.save_theme(user_theme)

        self.color_picker_items = []
        self.color_picker_items_squares = []

        top = Toplevel()
        top.config(bg=ACCENT)
        top.geometry("450x200")
        top.title("Color Configurer")
        top.focus_set()
        self.color_picker_items.append(top)

        # Define a dictionary to store the user theme colors
        user_theme = user_theme_config.load_theme()

        label_container = Canvas(top, width=200, height=150, bg=ACCENT, highlightthickness=0)
        label_container.place(x=15, y=25)
        self.color_picker_items.append(label_container)

        # Create labels for selecting colors
        bg_label = Label(label_container, text=None, width=4, height=2, highlightthickness=2,
                         highlightbackground=FONT_COLOR,
                         bg=user_theme["bg"])
        bg_label.bind("<Button-1>", lambda event: choose_color(bg_label, "bg"))
        bg_label.place(x=10, y=0)
        bg_text = Label(label_container, text="Background", bg=ACCENT, fg=FONT_COLOR, font=FONT)
        bg_text.place(x=65, y=5)
        self.color_picker_items_squares.append(bg_label)
        self.color_picker_items.append(bg_text)

        accent_label = Label(label_container, text=None, width=4, height=2, highlightthickness=2,
                             highlightbackground=FONT_COLOR,
                             bg=user_theme["accent"])
        accent_label.bind("<Button-1>", lambda event: choose_color(accent_label, "accent"))
        accent_label.place(x=0, y=bg_label.winfo_y() + accent_label.winfo_reqheight() - 5)
        accent_text = Label(label_container, text="Foreground", bg=ACCENT, fg=FONT_COLOR, font=FONT)
        accent_text.place(x=55, y=bg_label.winfo_y() + accent_label.winfo_reqheight())
        self.color_picker_items_squares.append(accent_label)
        self.color_picker_items.append(accent_text)

        text_label = Label(label_container, text=None, width=4, height=2, highlightthickness=2,
                           highlightbackground=FONT_COLOR,
                           bg=user_theme["text"])
        text_label.bind("<Button-1>", lambda event: choose_color(text_label, "text"))
        text_label.place(x=10, y=accent_label.winfo_y() + text_label.winfo_reqheight() + 30)
        text_text = Label(label_container, text="Text", bg=ACCENT, fg=FONT_COLOR, font=FONT)
        text_text.place(x=65, y=accent_label.winfo_y() + text_label.winfo_reqheight() + 35)
        self.color_picker_items_squares.append(text_label)
        self.color_picker_items.append(text_text)

        self.clf_canvas = Canvas(top, width=250, height=150, bg=user_theme["bg"], highlightthickness=2,
                                 highlightcolor="white")
        self.clf_canvas.place(x=185, y=25)
        self.clf = custom_ui.CustomLabelFrame(self.clf_canvas, width=200, height=100, text="Sample text",
                                              bg=user_theme["bg"],
                                              fill=user_theme["accent"],
                                              fg=user_theme["text"])
        self.clf.canvas.place(x=25, y=25)
        self.clf_button = custom_button.CustomButton(self.clf.canvas, text="Button", bg=user_theme["accent"])
        self.clf_button.canvas.place(x=45, y=40)

        self.apply_user_theme_button = custom_button.CustomButton(top, text="Apply", bg=ACCENT,
                                                                  button_type=custom_button.button,
                                                                  command=self.update_colors)
        self.apply_user_theme_button.canvas.place(x=55, y=150)

    def close_settings_window(self):
        self.settings_window_opened = False
        self.settings_window.destroy()

    def create_history_window(self):
        """
        Creates or focuses on an existing history window.

        If a history window already exists and is open, it brings it to focus.
        Otherwise, it creates a new history window.

        The history window displays previous processing data and provides an option to exit.
        """

        def on_mousewheel(event):
            if event.num == 5 or event.delta == -120:
                if self.history_scroll_canvas.yview()[1] < 1.0:
                    self.history_scroll_canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                if self.history_scroll_canvas.yview()[0] > 0.0:
                    self.history_scroll_canvas.yview_scroll(-1, "units")

        if self.history_window is not None:  # Check if history window already exists
            if self.history_window.winfo_exists():  # Check if the window is open
                self.history_window.focus_set()  # Bring existing window to focus
                return

        # Set flag indicating a new history window is opened
        self.history_window_opened = True

        # Retrieve previous processing data
        # history_list = processing.read_from_history()

        # Create a new history window
        self.history_window = Toplevel(self.win)
        self.history_window.title(self.lang["history"])
        self.history_window.configure(background=BGCOLOR)
        self.history_window.geometry(f"{HIS_WIN_WIDTH}x{HIS_WIN_HEIGHT}")
        self.history_window.resizable(False, False)
        self.history_window.focus_set()
        self.history_window.protocol("WM_DELETE_WINDOW", self.close_history_window)

        self.cards_list = []
        if self.history_scroll_canvas is not None:
            if self.history_scroll_canvas.winfo_exists():
                debug.log("[Interface] History canvas exists, destroying!")
                self.history_scroll_canvas.destroy()

        # Create a Canvas widget inside the Toplevel window
        self.history_scroll_canvas = Canvas(self.history_window, bg=BGCOLOR, highlightthickness=0)
        self.history_scroll_canvas.pack(side="left", fill="both", expand=True)

        # Create a scrollbar for the Canvas
        self.history_scrollbar = Scrollbar(self.history_window, orient="vertical",
                                           command=self.history_scroll_canvas.yview, bg=BGCOLOR)
        self.history_scrollbar.pack(side="right", fill="y")

        # Configure the Canvas to use the scrollbar
        self.history_scroll_canvas.configure(yscrollcommand=self.history_scrollbar.set)

        # Create a Frame widget inside the Canvas to contain the scrollable content
        self.history_frame = Frame(self.history_window, bg=BGCOLOR)
        self.history_scroll_canvas.create_window((0, 0), window=self.history_frame, anchor="nw")

        # Bind mouse wheel scrolling to the window
        self.history_scrollbar.bind("<MouseWheel>", on_mousewheel)
        self.history_window.bind("<MouseWheel>", on_mousewheel)
        self.history_scroll_canvas.bind("<MouseWheel>", on_mousewheel)

        # Add CardItem widgets to the Frame for each history entry
        self.cards_list = None
        self.cards_list = []
        self.history_entries = history_handler.load_entries()
        if self.history_entries:
            for entry in self.history_entries:
                print(entry)
                if "normalize" not in entry: entry["normalize"] = self.lang["no_data"]
                if "stabilize" not in entry: entry["stabilize"] = self.lang["no_data"]
                if "img_path" not in entry: entry["img_path"] = self.lang["no_data"]
                if "video_path" not in entry: entry["video_path"] = self.lang["no_data"]
                if "result_path" not in entry: entry["result_path"] = self.lang["no_data"]
                card = custom_ui.CardItem(self.history_frame, width=795 - self.history_scrollbar.winfo_reqwidth() * 2,
                                          height=200, title="",
                                          img_path=entry["first_frame_path"],
                                          video_path=entry["video_path"],
                                          result=entry["result"],
                                          norm=entry["normalize"],
                                          stab=entry["stabilize"],
                                          bg=BGCOLOR)
                self.cards_list.append(card)
                self.cards_list[len(self.cards_list) - 1].canvas.pack(padx=10, pady=10)

        # Update the scroll region of the Canvas
        self.history_frame.update_idletasks()
        self.history_scroll_canvas.config(scrollregion=self.history_scroll_canvas.bbox("all"))

    def close_history_window(self):
        """
        Closes the history window if it exists and logs its status.

        If the history window exists, it clears the content list, destroys the exit button,
        and destroys the history window. It then sets the status flag indicating the window's
        closure and logs its status. Additionally, it checks if the window still exists after
        destruction and logs the result.
        """
        if self.history_window is not None:  # Check if history window exists
            # print(f"Size of history window: {sys.getsizeof(self.history_window)} bytes")
            self.history_entries = None
            # print(f"Size of cards: {sys.getsizeof(self.cards_list)} bytes")
            # self.cards_list = []
            for elem in self.cards_list:
                elem.canvas.destroy()
            # print(f"Size of cards: {sys.getsizeof(self.cards_list)} bytes")
            self.history_scroll_canvas.destroy()
            self.history_window.destroy()  # Destroy history window
            # print(f"Size of history window: {sys.getsizeof(self.history_window)} bytes")
            self.history_window_opened = False  # Set status flag to closed

            debug.log(f"[Interface] History window opened status: {self.history_window_opened}")

            # Check if the window still exists
            if self.history_window.winfo_exists():
                debug.log("[Interface] History window still exists.")
            else:
                debug.log("[Interface] History window has been destroyed.")

    def change_language(self):
        """
        Change the language of the GUI elements based on the selected language.
        This method updates the text of labels, buttons, and other widgets
        to reflect the language change.

        """
        # Update text for wrapper labels
        if self.browse_wrapper is not None: self.browse_wrapper.set_label_text(self.lang["input_file"])
        if self.frame_wrapper is not None:
            self.frame_wrapper.set_label_text(self.lang["video_data"])
            self.prepass_toggle_button.config(text=self.lang["normalization"])
            self.stab_toggle_button.config(text=self.lang["stabilization"])
            self.plotting_toggle_button.config(text=self.lang["to_plot"])
        if self.proc_progress_wrapper is not None: self.proc_progress_wrapper.set_label_text(self.lang["progress"])
        if self.stab_progress_wrapper is not None: self.stab_progress_wrapper.set_label_text(self.lang["stabilization"])
        if self.prep_wrapper is not None: self.prep_wrapper.set_label_text(self.lang["preprocessing"])

        # Update text for specified widgets
        for label in [self.settings_window, self.button_wrapper, self.history_title, self.finished_window,
                      self.frame_wrapper, self.proc_progress_wrapper, self.settings_label, self.lang_label,
                      self.theme_label]:
            self.change_text(label)

        # Update text of history window
        if self.history_window is not None:
            if self.history_window.winfo_exists():
                for card in self.cards_list:
                    card.path_text.config(text="")
                    card.text.config(text="")
                    card.diff_text.config(text="")
                    card.diff_title.config(text="")
                    card.norm_text.config(text="")
                    card.stab_text.config(text="")
                    card.create_text(card.video_path, card.result)
                    card.process_button.set_text(self.lang["load_video"])

        # Update text of finished window
        if self.finished_window is not None:
            if self.finished_window.winfo_exists():
                self.finished_window.title(self.lang["proc_finished"])
                self.finished_title_label.config(text=self.lang["proc_finished"])
                self.result_label.config(text=f"{self.lang["diff"]}: {processing.total_difference}")

        # Set the selected language option based on current language
        self.lang_options = [self.lang["english"], self.lang["hungarian"]]
        if self.curr_lang == "english":
            self.lang_selected_option.set(self.lang_options[0])
        else:
            self.lang_selected_option.set(self.lang_options[1])

        # Set the selected theme option based on the current theme
        if self.curr_theme == "dark":
            self.theme_selected_option.set(self.theme_options[0])
        elif self.curr_theme == "light":
            self.theme_selected_option.set(self.theme_options[1])
        elif self.curr_theme == "palenight":
            self.theme_selected_option.set(self.theme_options[2])

        # Update text for buttons
        for button in [self.save_button, self.browse_button, self.browse_button, self.process_video_button,
                       self.media_player_button]:
            self.change_button_text(button)

        # Update frame details header
        if self.frame_details_header is not None:
            self.frame_details_header.config(text=self.lang["video_det"])

        # Update image details if available
        if self.im_det is not None:
            self.im_det = "\n".join(
                [f"{self.lang[key]}: {self.image_detail_dict[key]}"
                 for key, value in self.image_detail_dict.items()])
        if self.image_details is not None:
            self.image_details.config(text=self.im_det)

        # Update settings window
        if self.settings_window is not None:
            self.settings_window.title(self.lang["settings"])
            self.user_theme_button.config(text=self.lang["configure"])
            self.clear_history_button.config(text=self.lang["clear_history"])
            self.clear_video_button.config(text=self.lang["clear_video"])
        if self.settings_label is not None:
            self.settings_label.place(
                x=self.settings_wrapper.get_width() // 2 - self.settings_label.winfo_reqwidth() // 2,
                y=10)

        debug.log("[Interface] Texts updated!", text_color="blue")

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
            if not hasattr(widget, "keys") or not widget.keys:
                return
            if hasattr(widget, "winfo_exists"):
                if not widget.winfo_exists():
                    return
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

    def set_user_theme_colors(self):
        global USER_BG, USER_ACCENT, USER_FONT_COLOR
        utd = user_theme_config.load_theme()
        USER_BG, USER_ACCENT, USER_FONT_COLOR = utd["bg"], utd["accent"], utd["text"]

    def update_colors(self):
        """
        Update the colors of the GUI elements to match the current theme settings.
        This method sets the background and foreground colors of various widgets.
        """
        global BGCOLOR, ACCENT, FONT_COLOR
        self.set_user_theme_colors()
        self.set_color()

        if self.buttons_wrapper is not None:
            self.buttons_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR,
                                              buttons=[self.settings_button, self.history_button])

        if self.browse_wrapper is not None:
            self.browse_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR,
                                             buttons=[self.browse_button],
                                             labels=[self.opened_file_label])

        if self.frame_wrapper is not None:
            self.frame_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR,
                                            buttons=[self.media_player_button, self.process_video_button],
                                            labels=[self.frame_details_header, self.image_details])
            self.prepass_toggle_button.config(fg=FONT_COLOR, bg=ACCENT)
            self.stab_toggle_button.config(fg=FONT_COLOR, bg=ACCENT)
            self.plotting_toggle_button.config(fg=FONT_COLOR, bg=ACCENT)

        if self.terminal_wrapper is not None:
            self.terminal_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR)
            self.log_label_text.config(bg=ACCENT, fg=FONT_COLOR)
            self.log_canvas.config(bg=ACCENT)

        if self.proc_progress_wrapper is not None:
            self.proc_progress_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR, labels=[self.proc_progress_label])
            self.proc_progress_bar.config(bg=ACCENT)
            self.proc_pbar_overlay.config(fill=ACCENT, bg=ACCENT)

        if self.stab_progress_wrapper is not None:
            self.stab_progress_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR, labels=[self.stab_progress_label])
            self.stab_progress_bar.config(bg=ACCENT)
            self.stab_pbar_overlay.config(fill=ACCENT, bg=ACCENT)

        if self.prep_wrapper is not None:
            self.prep_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR, labels=[self.prep_progress_label])
            self.prep_progress_bar.config(bg=ACCENT)
            self.prep_pbar_overlay.config(fill=ACCENT, bg=ACCENT)

        if self.settings_wrapper is not None:
            self.settings_window.configure(bg=BGCOLOR)
            self.settings_wrapper.switch_theme(ACCENT, FONT_COLOR, BGCOLOR,
                                               buttons=[self.save_button, self.user_theme_button,
                                                        self.clear_video_button, self.clear_history_button],
                                               labels=[self.settings_label, self.lang_label, self.theme_label,
                                                       self.log_label])
            for option_menu in [self.theme_option_menu, self.lang_option_menu, self.log_option_menu]:
                option_menu.config(anchor="center", bg=ACCENT, fg=FONT_COLOR, activebackground=ACCENT,
                                   activeforeground=FONT_COLOR, highlightbackground=ACCENT)

            if self.color_picker_items is not None:
                for item in self.color_picker_items:
                    if item is not None:
                        if item.winfo_exists():
                            if isinstance(item, Toplevel) or isinstance(item, Canvas):
                                item.config(bg=ACCENT)
                            else:
                                item.config(bg=ACCENT, fg=FONT_COLOR)
                for item in self.color_picker_items_squares:
                    if item is not None:
                        if item.winfo_exists():
                            item.config(highlightbackground=FONT_COLOR)
            if self.apply_user_theme_button is not None:
                if self.apply_user_theme_button.canvas.winfo_exists():
                    self.apply_user_theme_button.config(bg=ACCENT)

        if self.history_window is not None and self.history_window.winfo_exists():
            self.history_scroll_canvas.config(bg=BGCOLOR)
            self.history_frame.config(bg=BGCOLOR)
            for card in self.cards_list:
                card.container.switch_theme(ACCENT, FONT_COLOR, BGCOLOR,
                                            labels=[card.diff_text, card.diff_title, card.path_text, card.text,
                                                    card.norm_title, card.norm_text, card.norm_title, card.stab_text,
                                                    card.stab_title, card.stab_title, card.stab_text],
                                            buttons=[card.process_button])
        else:
            if self.history_window is not None:
                self.history_window.destroy()

        if self.finished_window is not None and self.finished_window.winfo_exists():
            self.finished_window.config(bg=ACCENT)
            self.finished_title_label.config(bg=ACCENT, fg=FONT_COLOR)
            self.result_label.config(bg=ACCENT, fg=FONT_COLOR)
            self.ok_button.config(bg=ACCENT)

        # Set background color for the main window
        self.win["bg"] = BGCOLOR
        debug.log("[Interface] Colors updated!", text_color="blue")
