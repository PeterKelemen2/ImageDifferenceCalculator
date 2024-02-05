import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk


class MediaPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Player")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.frames = []
        self.current_frame = 0
        self.playing = False

        # Buttons
        self.open_button = tk.Button(self, text="Open Video", command=self.open_video)
        self.open_button.pack(pady=10)

        self.play_button = tk.Button(self, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(self, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT, padx=10)

    def open_video(self):
        file_path = filedialog.askopenfilename(title="Select a video file",
                                               filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv")])
        if file_path:
            self.frames = self.extract_frames(file_path)
            self.current_frame = 0
            self.display_frame()

    def extract_frames(self, file_path):
        cap = cv2.VideoCapture(file_path)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            frames.append(ImageTk.PhotoImage(image=image))
        cap.release()
        return frames

    def display_frame(self):
        if self.frames and 0 <= self.current_frame < len(self.frames):
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.frames[self.current_frame])

    def play_video(self):
        if self.frames:
            self.playing = True
            self.play_frames()

    def play_frames(self):
        if self.playing and 0 <= self.current_frame < len(self.frames):
            self.display_frame()
            self.current_frame += 1
            self.after(100, self.play_frames)
        else:
            self.playing = False

    def pause_video(self):
        self.playing = False
