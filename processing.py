import os
import threading
import time

import cv2
import numpy as np

import debug
import interface
import new_tracking
import opencv_stabilization
import stabilizer

progress_callback = None
progress_percentage = None
total_difference = None
is_finished = False
HISTORY_PATH = "processing_history.txt"


def set_progress_callback(callback):
    """
    Sets the progress callback function.

    This function sets the callback function that will be called during video processing
    to report progress.

    Parameters:
        callback (function): The callback function to report progress.
    """
    global progress_callback
    progress_callback = callback


def process_video(path, progress_callback):
    """
    Processes the video file.

    This function reads frames from the video file specified by `path`, calculates the difference
    between consecutive frames, and reports progress through the callback function.

    Parameters:
        path (str): The path to the video file.
        progress_callback (function): The callback function to report progress.
    """
    start_time = time.time()
    current_frame_index = 0
    frames_since_last_callback = 0

    # opencv_stabilization.stab_video_thread(path)
    #
    # while not opencv_stabilization.is_finished:
    #     time.sleep(0.02)

    new_tracking.stab_video_thread(path)

    while not new_tracking.is_finished:
        time.sleep(0.02)

    new_path = path[:-4] + ".mp4"
    new_path = path[:-4] + "_newly_stabilized.mp4"

    global total_difference, is_finished, progress_percentage
    total_difference = 0
    finished = False

    debug.log(f"Started processing {new_path}", text_color="blue")

    alpha = 50
    beta = 230
    contrast = 1.4
    brightness = 1.3
    threshold_upper_light = 130
    threshold_lower_light = 0
    threshold_upper_dark = 255
    threshold_lower_dark = 95
    thresh_method = cv2.THRESH_BINARY

    cap = cv2.VideoCapture(new_path)

    ret, first_frame = cap.read()
    first_frame_blurred = cv2.GaussianBlur(first_frame, (21, 21), 0)
    gray_frame = cv2.cvtColor(first_frame_blurred, cv2.COLOR_BGR2GRAY)
    binary_mask_light = cv2.inRange(gray_frame, threshold_lower_light, threshold_upper_light)
    binary_mask_dark = cv2.inRange(gray_frame, threshold_lower_dark, threshold_upper_dark)

    # _, first_frame = cv2.threshold(first_frame, threshold_upper_light, 255, thresh_method)
    # cv2.normalize(first_frame, first_frame, alpha, beta, cv2.NORM_MINMAX)

    height, width = first_frame.shape[:2]
    accumulated_frame = np.zeros((height, width, 3), dtype=np.float32)
    video_output = cv2.VideoWriter("C:/diff_video.mp4", cv2.VideoWriter_fourcc('F', 'F', 'V', '1'), 95, (width, height))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not cap.isOpened():
        debug.log("Could not open video", text_color="red")
    else:
        average1 = np.float32(first_frame)

        if not ret:
            debug.log("Could not read video frames", text_color="red")
        else:
            while True:
                current_frame_index += 1

                # Discarding of the 2ms pulse of light
                if current_frame_index == 3:
                    ret, frame = cap.read()
                    ret, frame = cap.read()
                    # cv2.normalize(frame, frame, alpha, beta, cv2.NORM_MINMAX)
                    # frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)
                    current_frame_index = 0
                else:
                    ret, frame = cap.read()
                    # cv2.normalize(frame, frame, alpha, beta, cv2.NORM_MINMAX)
                    # frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

                frames_since_last_callback += 1

                if not ret:
                    break

                # frame = cv2.GaussianBlur(frame, (7, 7), 0)
                # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #
                # binary_mask_light = cv2.inRange(gray_frame, threshold_lower_light, threshold_upper_light)
                # binary_mask_dark = cv2.inRange(gray_frame, threshold_lower_dark, threshold_upper_dark)

                first_mask_pass = cv2.bitwise_and(frame, frame, mask=binary_mask_light)
                second_mask_pass = cv2.bitwise_and(first_mask_pass, frame, mask=binary_mask_dark)

                cv2.accumulateWeighted(second_mask_pass, average1, 0.04)
                # accumulated_frame += second_mask_pass.astype(np.float32)
                frame_delta = cv2.absdiff(second_mask_pass, cv2.convertScaleAbs(accumulated_frame))
                video_output.write(frame_delta)
                # video_output.write(second_mask_pass)

                # cv2.imshow("Main video", cv2.resize(frame, (500, 500)))
                # cv2.imshow("Change in foreground", cv2.resize(frame_delta, (500, 500)))

                if frames_since_last_callback == 5:
                    progress_percentage = "{:.0f}".format((cap.get(cv2.CAP_PROP_POS_FRAMES) * 100) / total_frames)
                    progress_callback("processing", int(progress_percentage))
                    frames_since_last_callback = 0

                # first_frame = frame

            cap.release()
            video_output.release()
            cv2.destroyAllWindows()

            finished = True
            write_to_history(path, total_difference)
            debug.log(f"Processing finished in {"{:.2f}s".format(time.time() - start_time)}", text_color="cyan")
            progress_callback("processing", 100)


def process_video_thread(path):
    """
    Creates a thread for video processing.

    This function creates a separate thread to process the video specified by `path`.

    Parameters:
        path (str): The path to the video file.
    """
    global progress_callback
    if progress_callback is None:
        debug.log("Progress callback not set. Aborting video processing.", text_color="red")
        return
    thread = threading.Thread(target=process_video, args=(path, progress_callback))
    thread.start()


def init_history():
    """
    Initializes the processing history file.

    This function creates a new processing history file if it doesn't exist.
    """
    if not os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "w"):
                debug.log("History file created", text_color="blue")
        except Exception as e:
            debug.log(str(e), text_color="red")


def write_to_history(video_file: str, result):
    """
    Writes processing result to the history file.

    This function writes the processing result for a video file to the history file.

    Parameters:
        video_file (str): The path to the video file.
        result: The processing result.
    """
    file_name = video_file.split("/")
    with open(HISTORY_PATH, "a") as history_file:
        history_file.write(f"File: {file_name[len(file_name) - 1]};Result: {result}\n")


def read_from_history():
    """
    Reads processing history from the history file.

    This function reads the processing history from the history file and prints the last 7 entries.

    Returns:
        list: A list containing the last 7 entries from the history file.
    """
    res_list = list()
    with open(HISTORY_PATH, "r") as history_file:
        for line in history_file:
            res_list.append(line)

    # Show last 7 lines
    while len(res_list) > 7:
        res_list.pop(0)

    i = 0
    for line in res_list:
        i += 1
        print(f"{i} - {line.rstrip()}")
    return res_list
