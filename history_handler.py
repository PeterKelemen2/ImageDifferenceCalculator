import datetime
import json
import os
import shutil

import cv2

import debug

history_path = "history.json"


class HistoryEntry:
    def __init__(self, video_path=None, frame=None, result=None, normalize=None, stabilize=None):
        self.video_path = video_path
        if result is None:
            self.result = "Aborted."
        else:
            self.result = str(result)

        if self.video_path:
            self.video_path = str(video_path)

            if frame is not None:
                if not os.path.exists("history"):
                    os.mkdir("history")
                img_path = f"history/{self.video_path.split("/")[-1].split(".")[0]}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.jpg"
                self.first_frame_path = img_path
                cv2.imwrite(img_path, frame)

        if normalize is True or normalize is False:
            self.normalize = normalize

        if stabilize is True or stabilize is False:
            self.stabilize = stabilize

    def to_dict(self):
        return self.__dict__


def save_entry(entry):
    # Read existing data from the JSON file, if any
    if not os.path.exists("history"):
        os.mkdir("history")
    try:
        with open(history_path, "r") as json_file:
            history_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize history_data as an empty list
        history_data = []

    # Convert the entry to a dictionary
    entry_dict = entry.to_dict()

    # Append the new entry to the existing data
    history_data.append(entry_dict)

    # Write the updated data back to the JSON file
    with open(history_path, "w") as json_file:
        json.dump(history_data, json_file, indent=4)


def load_entries():
    if os.path.exists(history_path):
        try:
            with open(history_path, "r") as json_file:
                history_data = json.load(json_file)
            return history_data
        except FileNotFoundError:
            return []
    else:
        try:
            with open(history_path, "w") as json_file:
                json_file.write("[\n]")
        except FileNotFoundError:
            return []


def clear_history():
    debug.log("[History] Clearing history")
    if os.path.exists(history_path):
        os.remove(history_path)
    if os.path.exists("history"):
        shutil.rmtree("history")
    else:
        debug.log("[History] No history found")
