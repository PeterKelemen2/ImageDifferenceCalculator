import datetime
import os
import shutil
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
stop_thread_event: threading.Event = None
callback_queue: Queue = Queue()
force_terminate = False
processing_folder = "processed-videos"
processed_path = ""

video_writer = None


def get_result():
    return total_difference


def set_progress_callback(callback):
    global progress_callback
    progress_callback = callback


def create_highlighted_frame(frame, roi):
    ratio = 6
    n_h, n_w = frame.shape[0] // ratio, frame.shape[1] // ratio
    s_roi = (roi[0] // ratio, roi[1] // ratio, roi[2] // ratio, roi[3] // ratio)
    frame = cv2.resize(frame, (n_w, n_h))
    return cv2.rectangle(frame, (s_roi[0], s_roi[1]), (s_roi[0] + s_roi[2], s_roi[1] + s_roi[3]), (0, 255, 0), 2)


def process_video(path, preprocess, stabilize, to_plot, p_callback):
    global is_finished, total_difference, progress_percentage, stop_thread_event, initialized, video_writer

    initialized = True
    is_finished = False
    stop_thread_event = threading.Event()

    if not is_finished:
        start_time = time.time()
        if preprocess or stabilize:
            date = f"{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}"
            global processed_path
            if not os.path.exists(processing_folder):
                os.mkdir(processing_folder)
            processed_path = f"{processing_folder}/{path.split("/")[-1].split(".")[0]}-{date}"
            os.mkdir(processed_path)

        if stabilize or preprocess:
            video_stabilization.set_progress_callback(p_callback)
            debug.log("[Processing] Starting stabilization thread...")
            video_stabilization.stab_video_thread(path, to_plot, stabilize, preprocess)
            while not video_stabilization.is_finished:
                time.sleep(0.02)
            video_stabilization.thread.join()
        debug.log("[Processing] Stabilization finished!")

        new_path = f"{processed_path}/{path.split("/")[-1]}"

    total_difference = 0
    if not stop_thread_event.is_set():
        if not stabilize and not preprocess:
            debug.log(f"[Processing] Started processing {path}", text_color="blue")
            new_path = path

        print(new_path)
        cap = cv2.VideoCapture(new_path)
        ret, prev_frame = cap.read()
        first_frame = prev_frame
        if not ret:
            debug.log(f"[Processing] Unable to read the video file.")

        new_roi = cv2.selectROI("Select ROI", prev_frame)
        cv2.destroyWindow("Select ROI")
        proc_time = time.time()
        debug.log(f"[Processing] ROI: {new_roi}")

        x, y, w, h = new_roi
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cropped_output_path = new_path[:-4] + "_processed.mp4"
        codec = cv2.VideoWriter_fourcc(*'x264')
        video_writer = cv2.VideoWriter(cropped_output_path, codec, int(cap.get(cv2.CAP_PROP_FPS)), (w, h))

        history_frame = create_highlighted_frame(first_frame, new_roi)
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
            diff_rgb = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
            video_writer.write(diff_rgb)

            # Calculate Mean Squared Error (MSE)
            total_mean += np.mean((diff / 255.0) ** 2)

            if current_frame_index % 2 == 0:
                callback_queue.put(lambda: p_callback("processing", (current_frame_index * 100) // total_frames))

        cap.release()
        video_writer.release()
        callback_queue.put(lambda: p_callback("processing", 100))
        total_difference = total_mean / total_frames
        debug.log(f"[Processing] Total difference: {total_difference}")

        is_finished = True
        if total_difference <= 0:
            total_difference = "Aborted."
        history_handler.save_entry(
            history_handler.HistoryEntry(video_path=path,
                                         frame=history_frame,
                                         result=total_difference,
                                         normalize=preprocess,
                                         stabilize=stabilize))

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
        global force_terminate
        force_terminate = True
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


def clear_processed_videos():
    debug.log("[Processing] Removing previously processed videos...")
    if os.path.exists(processing_folder):
        shutil.rmtree(processing_folder)
    else:
        debug.log("[Processing] No previous video processing folder found!")
        return
    debug.log("[Processing] Removal successful!")
