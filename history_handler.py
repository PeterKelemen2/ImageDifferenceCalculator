import json

import cv2


class HistoryEntry:
    def __init__(self, video_path=None, result=None, normalize=None, stabilize=None):
        self.video_path = video_path
        if result is None:
            self.result = "Aborted."
        else:
            self.result = str(result)

        if self.video_path:
            video = cv2.VideoCapture(self.video_path)
            ret, first_frame = video.read()
            if ret:
                width, height = first_frame.shape[:2]
                frame_to_write = cv2.resize(first_frame, (height // 4, width // 4))
                cv2.imwrite("history/" + self.video_path.split("/")[-1] + ".jpg", frame_to_write)
                self.first_frame_path = "history/" + self.video_path.split("/")[-1] + ".jpg"

        if normalize is not None:
            self.normalize = normalize
        if stabilize is not None:
            self.stabilize = stabilize

    def to_dict(self):
        return self.__dict__


def save_entry(entry):
    # Read existing data from the JSON file, if any
    try:
        with open("history.json", "r") as json_file:
            history_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize history_data as an empty list
        history_data = []

    # Convert the entry to a dictionary
    entry_dict = entry.to_dict()

    # Append the new entry to the existing data
    history_data.append(entry_dict)

    # Write the updated data back to the JSON file
    with open("history.json", "w") as json_file:
        json.dump(history_data, json_file, indent=4)


def load_entries():
    try:
        with open("history.json", "r") as json_file:
            history_data = json.load(json_file)
        return history_data
    except FileNotFoundError:
        print("Error: History file not found.")
        return []
