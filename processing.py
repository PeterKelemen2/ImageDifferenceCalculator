import os
from queue import Queue
import sys
import threading
import time

import cv2
import numpy as np

import debug
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
        if preprocess:
            prep_start_time = time.time()
            prepass.set_progress_callback(p_callback)
            prepass.preprocess_video_thread(path, to_plot)
            debug.log("[Processing] Started preprocessing thread!")
            while not prepass.is_finished:
                time.sleep(0.02)
            prepass.thread.join()
            debug.log(f"[Processing] Preprocessing!")
            new_path = new_path[:-4] + "_prepass.mp4"

        if stabilize:
            video_stabilization.set_progress_callback(p_callback)
            debug.log("[Processing] Starting stabilization thread...")
            video_stabilization.stab_video_thread(new_path, to_plot)
            while not video_stabilization.is_finished:
                time.sleep(0.02)
            video_stabilization.thread.join()
            debug.log("[Processing] Stabilization finished!")
            new_path = path[:-4] + "_prepass_stabilized.mp4"

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
                write_to_history(path, total_difference)
            else:
                write_to_history(path, "Aborted.")
            debug.log(
                f"[Processing] Image difference calculation finished in {"{:.2f}s".format(time.time() - proc_time)}",
                text_color="cyan")
            debug.log(f"[Processing] Total processing finished in {"{:.2f}s".format(time.time() - start_time)}",
                      text_color="cyan")

        # cap = cv2.VideoCapture(new_path)
        # ret, first_frame = cap.read()
        # if first_frame is not None or not stop_thread_event.is_set():
        #     avg_light_level = first_frame.sum() // first_frame.size
        #
        #     threshold_lower_light = 0
        #     threshold_upper_light = int(avg_light_level + avg_light_level * 0.18)
        #     threshold_lower_dark = int(avg_light_level - avg_light_level * 0.18)
        #     threshold_upper_dark = 255
        #
        #     debug.log(f"{avg_light_level} {threshold_upper_light} {threshold_lower_dark}")
        #
        #     first_frame_blurred = cv2.GaussianBlur(first_frame, (21, 21), 0)
        #     gray_frame = cv2.cvtColor(first_frame_blurred, cv2.COLOR_BGR2GRAY)
        #     binary_mask_light = cv2.inRange(gray_frame, threshold_lower_light, threshold_upper_light)
        #     binary_mask_dark = cv2.inRange(gray_frame, threshold_lower_dark, threshold_upper_dark)
        #
        #     height, width = first_frame.shape[:2]
        #     accumulated_frame = np.zeros((height, width, 3), dtype=np.float32)
        #     new_path = new_path[:-4] + "_processed.mp4"
        #     video_output = cv2.VideoWriter("C:/diff_video.mp4", cv2.VideoWriter_fourcc('F', 'F', 'V', '1'), 95,
        #                                    (width, height))
        #     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #
        # if not cap.isOpened():
        #     debug.log("[Processing] Could not open video", text_color="red")
        #     is_finished = True
        #     stop_thread_event.set()
        #     cap.release()
        #     video_output.release()
        #     return
        # else:
        #     average1 = np.float32(first_frame)
        #
        #     if not ret:
        #         debug.log("[Processing] Could not read video frames", text_color="red")
        #         is_finished = True  # Ensure is_finished is updated even if an error occurs
        #         stop_thread_event.set()  # Set stop event in case of error
        #         cap.release()
        #         video_output.release()
        #         return
        #
        #     while not stop_thread_event.is_set():
        #         current_frame_index += 1
        #
        #         ret, frame = cap.read()
        #         if not ret:
        #             break
        #         frames_since_last_callback += 1
        #
        #         first_mask_pass = cv2.bitwise_and(frame, frame, mask=binary_mask_light)
        #         second_mask_pass = cv2.bitwise_and(first_mask_pass, frame, mask=binary_mask_dark)
        #
        #         cv2.accumulateWeighted(second_mask_pass, average1, 0.04)
        #         frame_delta = cv2.absdiff(second_mask_pass, cv2.convertScaleAbs(accumulated_frame))
        #         # video_output.write(frame_delta)
        #         video_output.write(frame)
        #
        #         if frames_since_last_callback == 5:
        #             progress_percentage = "{:.0f}".format(
        #                 (cap.get(cv2.CAP_PROP_POS_FRAMES) * 100) / total_frames)
        #             callback_queue.put(lambda: p_callback("processing", int(progress_percentage)))
        #             frames_since_last_callback = 0
        #             debug.log(f"[Processing] Processing {progress_percentage}%")
        #
        #     cap.release()
        #     video_output.release()
        #     cv2.destroyAllWindows()
        #
        #     callback_queue.put(lambda: p_callback("processing", 100))
        #     # is_finished = True
        #
        #     write_to_history(path, total_difference)
        #     debug.log(f"[Processing] Processing finished in {"{:.2f}s".format(time.time() - start_time)}",
        #               text_color="cyan")
        #     # new_frame = path
        #
        #     processed_video_cap = cv2.VideoCapture("C:/diff_video.mp4")
        #     ret, prev_frame = processed_video_cap.read()
        #     if not ret:
        #         debug.log(f"[Processing] Unable to read the video file.")
        #
        #     new_roi = cv2.selectROI("Select ROI", prev_frame)
        #     cv2.destroyWindow("Select ROI")
        #
        #     debug.log(f"[Processing] ROI: {new_roi}")
        #
        #     x, y, w, h = new_roi
        #     cropped_output_path = "C:/cropped.mp4"
        #     codec = cv2.VideoWriter_fourcc('F', 'F', 'V', '1')
        #     cropped_video_writer = cv2.VideoWriter(cropped_output_path, codec, 95, (w, h))
        #
        #     # processed_video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #
        #     prev_gray_cropped = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)[y:y + h, x:x + w]
        #     # debug.log(f"[Processing] Previous gray: {prev_gray.shape[:2]}")
        #     # prev_gray = prev_gray[y:y + h, x:x + w]  # Cropped
        #     # debug.log(f"[Processing] Previous gray after crop: {prev_gray.shape[:2]}")
        #
        #     while not stop_thread_event.is_set():
        #         ret, frame = processed_video_cap.read()
        #         if not ret:
        #             break
        #         # cropped_frame = frame[y:y + h, x:x + w]
        #         # gray_cropped = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        #
        #         gray_cropped = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y:y + h, x:x + w]
        #         diff = cv2.absdiff(gray_cropped, prev_gray_cropped)
        #
        #         _, threshold_diff = cv2.threshold(diff, int(avg_light_level), 255, cv2.THRESH_BINARY)
        #
        #         prev_gray_cropped = gray_cropped
        #
        #         cropped_video_writer.write(diff)
        #
        #         cv2.imshow("Cropped frame", threshold_diff)
        #         # cv2.imshow("Cropped frame", diff)
        #
        #         key = cv2.waitKey(1) & 0xFF
        #         if key == ord('q'):
        #             break
        #
        #     cropped_video_writer.release()
        #     processed_video_cap.release()
        #
        #     is_finished = True
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
