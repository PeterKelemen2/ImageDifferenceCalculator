import os
import sys
import threading
import time
from queue import Queue

import debug

import cv2
import numpy as np

import plotting
import processing

is_finished = False
initialized = False
progress_callback = None
stop_thread = False
callback_queue: Queue = Queue()
thread: threading.Thread = None
stop_thread_event: threading.Event = None
force_stopped = False


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


def preprocess(path, to_plot=True):
    global is_finished, stop_thread_event, progress_callback, initialized
    initialized = True
    p_callback = progress_callback
    stop_thread_event = threading.Event()

    if not is_finished:
        debug.log("Entered preprocess method")
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

        while not stop_thread_event.is_set():
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
                processing.callback_queue.put(
                    lambda: p_callback("preprocessing", int("{:.0f}".format((curr_index * 100) / total_frames))))
                # p_callback("preprocessing", int("{:.0f}".format((curr_index * 100) / total_frames)))
                # debug.log("{:.0f}".format((curr_index * 100) / total_frames))

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
        processing.callback_queue.put(lambda: p_callback("preprocessing", 100))
        # execute_callbacks()
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


def stop_prepass_thread():
    global thread, stop_thread_event, is_finished, force_stopped

    if stop_thread_event is not None:
        stop_thread_event.set()
        force_stopped = True
        time.sleep(0.5)  # To wait for the current cycle to finish
        debug.log("Preprocessing Thread event set!")

    if thread is not None:
        debug.log("Joining preprocessing thread...")
        if stop_thread_event is not None and stop_thread_event.is_set():
            thread.join()
        debug.log("Preprocessing thread joined!")

    is_finished = True

    debug.log("Stopped preprocessing thread!", text_color="blue")


def execute_callbacks():
    debug.log("Executing preprocessing callbacks...", text_color="blue")
    while not callback_queue.empty():
        callback = callback_queue.get()
        callback()
        # debug.log(f"Executed {callback} callback")


def preprocess_video_thread(path, to_plot):
    """
    Creates a thread for video processing.

    This function creates a separate thread to process the video specified by `path`.

    Parameters:
        path (str): The path to the video file.
    """
    global progress_callback, thread
    # if progress_callback is None:
    #     debug.log("Progress callback not set. Aborting video processing.", text_color="red")
    #     return
    thread = threading.Thread(target=preprocess, args=(path, to_plot))
    thread.start()
