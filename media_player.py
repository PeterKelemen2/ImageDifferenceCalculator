from tkinter import Canvas, Button
from PIL import Image, ImageTk
import cv2


class MediaPlayer:
    def __init__(self, master, file_path):
        self.master = master
        self.file_path = file_path
        self.master.title("Video Player")

        self.canvas = Canvas(master)
        self.canvas.pack()

        self.video_path = None
        self.cap = None

        self.playing = False
        self.paused = False
        self.framerate = None

        self.photo = None  # Store PhotoImage object

        self.play_button = Button(master, text="Play", command=self.toggle_play)
        self.play_button.pack(side="left", padx=10)

        self.stop_button = Button(master, text="Stop", command=self.stop_video)
        self.stop_button.pack(side="left", padx=10)

        self.open_button = Button(master, text="Open Video", command=self.open_video)
        self.open_button.pack(side="left", padx=10)

        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

    def open_video(self):
        if self.file_path:
            self.video_path = self.file_path
            self.cap = cv2.VideoCapture(self.video_path)
            self.framerate = int(1000 / self.cap.get(cv2.CAP_PROP_FPS))  # Delay in milliseconds
            self.play_video()

    def play_video(self):
        if self.cap is not None:
            self.playing = True
            while self.playing:
                ret, frame = self.cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame_rgb)
                    self.photo = ImageTk.PhotoImage(image=image)
                    self.canvas.config(width=image.width // 2, height=image.height // 2)
                    self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
                    self.master.update()
                    if not self.paused:
                        self.master.after(self.framerate)
                else:
                    self.stop_video()
                    break

    def toggle_play(self):
        if self.cap is not None:
            if self.playing:
                self.paused = not self.paused

    def stop_video(self):
        self.playing = False
        self.paused = False
        if self.cap is not None:
            self.cap.release()
            self.canvas.delete("all")

    def close_window(self):
        self.stop_video()
        self.master.destroy()