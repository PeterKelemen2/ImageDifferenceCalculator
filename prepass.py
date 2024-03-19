import os
import threading
import time

import debug

import cv2
import numpy as np

import plotting


def calculate_avg_brightness(frame):
    # return frame.sum() // frame.size
    return np.mean(frame)


def print_as_table_row(i, curr, first, delta, to_debug=False):
    # print(
    #     f"[{i}] {curr} (Difference: {curr - first} | {delta})")

    index_space = 4 - len(str(i))
    curr_space = 22 - len(str(curr))
    diff_space = 22 - len(str(curr - first))
    delta_space = 22 - len(str(delta))

    line = (" | " + " " * index_space + str(i) +
            " | " + " " * curr_space + str(curr) +
            " | " + " " * diff_space + str(curr - first) +
            " | " + " " * delta_space + str(delta))

    if to_debug:
        color = "blue"
        if i % 2 == 0:
            color = "magenta"
        debug.log(line, text_color=color)
    else:
        print(line)


is_finished = False
progress_callback = None
thread = None
stop_thread = False


def preprocess(path, p_callback, to_plot=True):
    start_time = time.time()

    cap = cv2.VideoCapture(path)

    new_path = path[:-4] + '_prepass.mp4'
    ret, first_frame = cap.read()
    frame_height, frame_width = first_frame.shape[:2]
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    codec = cv2.VideoWriter_fourcc(*'H264')
    output = cv2.VideoWriter(new_path, codec, 95, (frame_width, frame_height))

    curr_index = 0
    first_frame_brightness = calculate_avg_brightness(first_frame)

    b_list, prepass_b_list = [], []

    debug.log("Starting preprocessing...")

    global stop_thread
    while True:
        if stop_thread:
            return

        ret, frame = cap.read()
        if not ret:
            break
        curr_index += 1

        curr_brightness = calculate_avg_brightness(frame)
        b_list.append(curr_brightness)

        delta_brightness = 1 - ((curr_brightness - first_frame_brightness) / curr_brightness)
        # delta_brightness = round(1 - ((curr_brightness - first_frame_brightness) / curr_brightness), 4)
        if curr_brightness - first_frame_brightness == 0:
            delta_brightness = 1

        print_as_table_row(curr_index, curr_brightness, first_frame_brightness, delta_brightness, to_debug=True)

        frame = cv2.convertScaleAbs(frame, alpha=delta_brightness, beta=0)
        prepass_b_list.append(calculate_avg_brightness(frame))

        output.write(frame)

        if (curr_index % 10) % 5 == 0:
            p_callback("preprocessing", int("{:.0f}".format((curr_index * 100) / total_frames)))

    cap.release()
    output.release()
    if to_plot:
        debug.log("Creating graph for brightness regulation...", text_color="yellow")
        plotting.plot_average_brightness(before_list=b_list,
                                         after_list=prepass_b_list,
                                         title="Brightness regulation",
                                         path=path)
        # plotting.plot(values=[b_list, prepass_b_list],
        #               title="Brightness regulation",
        #               graph_labels=["Frame index", "Brightness value"],
        #               legend_labels=["Before", "After"],
        #               path=path)
        debug.log("Graph created!", text_color="yellow")
    debug.log(f"Preprocessing finished in {"{:.2f}s".format(time.time() - start_time)}", text_color="cyan")

    global is_finished
    is_finished = True


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


def kill_thread():
    global stop_thread
    stop_thread = True


def preprocess_video_thread(path, to_plot):
    """
    Creates a thread for video processing.

    This function creates a separate thread to process the video specified by `path`.

    Parameters:
        path (str): The path to the video file.
    """
    global progress_callback, thread
    if progress_callback is None:
        debug.log("Progress callback not set. Aborting video processing.", text_color="red")
        return
    thread = threading.Thread(target=preprocess, args=(path, progress_callback, to_plot))
    thread.start()
