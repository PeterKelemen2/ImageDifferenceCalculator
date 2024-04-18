import os
from queue import Queue
import sys
import threading
import time

import cv2
import numpy as np

import debug
import history_handler
import interface
import prepass
import video_stabilization

progress_callback = None
progress_percentage = None
total_difference = None
is_finished = False
initialized = False
thread: threading.Thread = None
HISTORY_PATH = "processing_history.txt"
stop_thread_event: threading.Event = None
callback_queue: Queue = Queue()


def get_result():
    return total_difference


def set_progress_callback(callback):
    global progress_callback
    progress_callback = callback


def process_video(path, preprocess, stabilize, to_plot, p_callback):
    global is_finished, total_difference, progress_percentage, stop_thread_event, initialized

    initialized = True
    is_finished = False
    stop_thread_event = threading.Event()

    if not is_finished:
        start_time = time.time()

        new_path = path
        # if preprocess:
        #     prep_start_time = time.time()
        #     prepass.set_progress_callback(p_callback)
        #     prepass.preprocess_video_thread(path, to_plot)
        #     debug.log("[Processing] Started preprocessing thread!")
        #     while not prepass.is_finished:
        #         time.sleep(0.02)
        #     prepass.thread.join()
        #     debug.log(f"[Processing] Preprocessing!")
        #     new_path = new_path[:-4] + "_prepass.mp4"

        if stabilize:
            video_stabilization.set_progress_callback(p_callback)
            debug.log("[Processing] Starting stabilization thread...")
            video_stabilization.stab_video_thread(new_path, to_plot, preprocess)
            while not video_stabilization.is_finished:
                time.sleep(0.02)
            video_stabilization.thread.join()
            debug.log("[Processing] Stabilization finished!")
            # new_path = path[:-4] + "_prepass_stabilized.mp4"
            new_path = path[:-4] + "_stabilized.mp4"

        total_difference = 0
        if not stop_thread_event.is_set():
            debug.log(f"[Processing] Started processing {new_path}", text_color="blue")

            cap = cv2.VideoCapture(new_path)
            ret, prev_frame = cap.read()
            if not ret:
                debug.log(f"[Processing] Unable to read the video file.")

            new_roi = cv2.selectROI("Select ROI", prev_frame)
            # new_roi = (387, 491, 271, 256)
            cv2.destroyWindow("Select ROI")
            proc_time = time.time()
            debug.log(f"[Processing] ROI: {new_roi}")

            x, y, w, h = new_roi
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cropped_output_path = new_path[:-4] + "_processed.mp4"
            codec = cv2.VideoWriter_fourcc('F', 'F', 'V', '1')
            video_writer = cv2.VideoWriter(cropped_output_path, codec, 95, (w, h))

            prev_gray_cropped = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)[y:y + h, x:x + w]

            total_mean = 0

            current_frame_index = 0

            while not stop_thread_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                current_frame_index += 1

                gray_cropped = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y:y + h, x:x + w]
                diff = cv2.absdiff(gray_cropped, prev_gray_cropped)
                video_writer.write(diff)

                # Calculate Mean Squared Error (MSE)
                total_mean += np.mean((diff / 255.0) ** 2)

                if current_frame_index % 2 == 0:
                    callback_queue.put(lambda: p_callback("processing", (current_frame_index * 100) // total_frames))

            video_writer.release()
            cap.release()
            cv2.destroyAllWindows()
            callback_queue.put(lambda: p_callback("processing", 100))
            total_difference = total_mean / total_frames
            debug.log(f"[Processing] Total difference: {total_difference}")

            is_finished = True
            if total_difference > 0:
                # write_to_history(path, total_difference)
                history_handler.save_entry(history_handler.HistoryEntry(video_path=path, result=total_difference))
            else:
                # write_to_history(path, "Aborted.")
                history_handler.save_entry(history_handler.HistoryEntry(video_path=path, result="Aborted."))
            debug.log(
                f"[Processing] Image difference calculation finished in {"{:.2f}s".format(time.time() - proc_time)}",
                text_color="cyan")
            debug.log(f"[Processing] Total processing finished in {"{:.2f}s".format(time.time() - start_time)}",
                      text_color="cyan")

    debug.log("[Processing] End of processing method")


def stop_processing_thread():
    global thread, stop_thread_event, progress_callback

    if prepass.stop_thread_event is not None:
        prepass.stop_thread_event.set()
        time.sleep(0.1)
        debug.log("[Processing] Preprocessing stop event set!")

    if video_stabilization.stop_thread_event is not None:
        video_stabilization.stop_thread_event.set()
        time.sleep(0.1)
        debug.log("[Processing] Video stabilization stop event set!")

    if stop_thread_event is not None:
        stop_thread_event.set()
        time.sleep(0.1)  # To wait for the current cycle to finish
        debug.log("[Processing] Main processing thread event set!")

    if thread is not None:
        debug.log("[Processing] Joining main processing thread...")
        if stop_thread_event is not None and stop_thread_event.is_set():
            thread.join()
        debug.log("[Processing] Main processing thread joined!")

    debug.log("[Processing] Stopped main processing thread!", text_color="blue")


def execute_callbacks():
    # debug.log("[Processing] Executing processing callbacks...", text_color="blue")
    while not callback_queue.empty():
        callback = callback_queue.get()
        callback()
        # debug.log(f"Executed {callback} callback")


def process_video_thread(path, prepass, stabilize, to_plot, callback):
    global progress_callback, thread
    progress_callback = callback
    # if progress_callback is None:
    if callback is None:
        debug.log("[Processing] Progress callback not set. Aborting video processing.", text_color="red")
        return
    debug.log(f"[Processing] Starting processing with Preprocess: {prepass}, Stabilization: {stabilize}")
    thread = threading.Thread(target=process_video, args=(path, prepass, stabilize, to_plot, callback))
    thread.start()


def init_history():
    if not os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "w"):
                debug.log("[Processing] History file created", text_color="blue")
        except Exception as e:
            debug.log(str(e), text_color="red")


def write_to_history(video_file: str, result):
    file_name = video_file.split("/")
    with open(HISTORY_PATH, "a") as history_file:
        history_file.write(f"File: {file_name[len(file_name) - 1]};Result: {result}\n")


def read_from_history():
    res_list = list()
    with open(HISTORY_PATH, "r") as history_file:
        for line in history_file:
            res_list.append(line)

    while len(res_list) > 7:
        res_list.pop(0)

    i = 0
    for line in res_list:
        i += 1
        print(f"{i} - {line.rstrip()}")
    return res_list
