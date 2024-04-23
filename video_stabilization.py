import sys
import threading
import time
from queue import Queue
import cv2
import numpy as np

import debug
import interface
import plotting
import prepass
import processing
import table_print

progress_callback = None
is_finished = False
thread: threading.Thread = None
stop_thread_event: threading.Event = None


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


# Function to find offset and move the frame
def stabilize_video(video_path, to_plot, stabilize, normalize, p_callback=None):
    global is_finished, stop_thread, stop_thread_event
    stop_thread_event = threading.Event()
    is_finished = False

    start_time = time.time()

    if not is_finished:
        # Read video input
        cap = cv2.VideoCapture(video_path)
        cv2.setNumThreads(16)
        output = f"{processing.processed_path}/{video_path.split("/")[-1]}"
        # output = processing.processed_path

        # Read the first frame
        ret, first_frame = cap.read()
        frame_height, frame_width = first_frame.shape[:2]

        resized_first_frame = cv2.resize(first_frame, (frame_width // 2, frame_height // 2))
        resized_frame_height, resized_frame_width = resized_first_frame.shape[:2]

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Calculate the position and dimensions of the ROI
        roi_width, roi_height = resized_frame_width // 4, resized_frame_height // 4
        roi_x = (resized_frame_width - roi_width) // 2
        roi_y = (resized_frame_height - roi_height) // 2

        # Crop the ROI from the first frame
        template = resized_first_frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # Define the output video codec and create a VideoWriter object
        codec = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(output, codec, int(cap.get(cv2.CAP_PROP_FPS)), (frame_width, frame_height))

        b_list, prepass_b_list = [], []
        if normalize:
            brightness_value = prepass.calculate_avg_brightness(first_frame)

        curr_frame_index = 1
        movement_data = []
        table_print.stab_table_print("Frame", "Total")

        frame_since_callback = 0
        while not stop_thread_event.is_set():

            frame_since_callback += 1
            if frame_since_callback == 3:
                table_print.stab_table_print(curr_frame_index, total_frames)
                processing.callback_queue.put(
                    lambda: p_callback("stabilization", int("{:.0f}".format((curr_frame_index * 100) / total_frames))))
                frame_since_callback = 0

            # Read the current frame
            ret, frame = cap.read()
            if ret:
                if normalize:
                    normalized_frame = prepass.normalized_frame(frame, brightness_value)
                    if to_plot:
                        b_list.append(prepass.calculate_avg_brightness(frame))
                        prepass_b_list.append(prepass.calculate_avg_brightness(normalized_frame))
                else:
                    normalized_frame = frame
                # Creating a half sized frame to use for the template matching
                resized_frame = cv2.resize(normalized_frame, (resized_frame_width, resized_frame_height))

            else:
                break

            if stabilize:
                # Draw the ROI rectangle on the current frame
                # cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

                # Use template matching to find the template in the current frame
                # result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
                result = cv2.matchTemplate(resized_frame, template, cv2.TM_CCOEFF_NORMED)
                _, _, _, max_loc = cv2.minMaxLoc(result)

                # Calculate the offset with scaling factor and negate the values
                offset = (-2 * (max_loc[0] - roi_x), -2 * (max_loc[1] - roi_y))
                # offset = (-1 * (max_loc[0] - roi_x), -1 * (max_loc[1] - roi_y))
                if to_plot:
                    movement_data.append(offset)
                # Move the frame by applying the offset
                M = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
                moved_frame = cv2.warpAffine(normalized_frame, M,
                                             (normalized_frame.shape[1], normalized_frame.shape[0]))
                # moved_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

                # Write the processed frame to the output video file
                out.write(moved_frame)
            else:
                out.write(normalized_frame)
            curr_frame_index += 1

        cap.release()
        out.release()

        processing.callback_queue.put(
            lambda: p_callback("stabilization", 100))
        # execute_callbacks()
        is_finished = True
        debug.log(f"[Stabilization] Stabilization finished in {"{:.2f}s".format(time.time() - start_time)}\n",
                  text_color="cyan")
        if to_plot:
            plotting.plot_stabilization_movement(movement_data=movement_data,
                                                 path=video_path[:-4] + "stabilization_plot.png")
            debug.log("[Stabilization] Stabilization movement plotted")

            debug.log("[Preprocessing] Creating graph for brightness regulation...", text_color="yellow")
            plotting.plot_average_brightness(before_list=b_list,
                                             after_list=prepass_b_list,
                                             path=video_path[:-4] + "normalization_plot.png")

            debug.log("[Preprocessing] Plot created!", text_color="yellow")


def stop_stabilization_thread():
    global thread, stop_thread_event

    if stop_thread_event is not None:
        stop_thread_event.set()
        time.sleep(0.2)  # To wait for the current cycle to finish
        debug.log("[Stabilization] Stabilization thread event set!")

    if thread is not None:
        debug.log("[Stabilization] Joining stabilization thread...")
        if stop_thread_event is not None and stop_thread_event.is_set():
            thread.join()
        debug.log("[Stabilization] Stabilization thread joined!")

    debug.log("[Stabilization] Stopped stabilization thread!", text_color="blue")


def stab_video_thread(path, to_plot, stabilize, normalize):
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
    thread = threading.Thread(target=stabilize_video, args=(path, to_plot, stabilize, normalize, progress_callback))
    thread.start()
