import threading
import time

import cv2

import debug
import interface

progress_callback = None
progress_percentage = None
total_difference = None
finished = False


def set_progress_callback(callback):
    global progress_callback
    progress_callback = callback


def process_video(path, progress_callback):
    start_time = time.time()
    current_frame_index = 0
    frames_since_last_callback = 0

    global total_difference
    total_difference = 0

    global finished
    finished = False

    global progress_percentage

    debug.log(f"Started processing of: {path}", text_color="blue")
    cap = cv2.VideoCapture(path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not cap.isOpened():
        debug.log("Could not open video", text_color="red")
    else:
        ret, prev_frame = cap.read()

        if not ret:
            debug.log("Could not read the first frame", text_color="red")
        else:
            while True:
                ret, frame = cap.read()
                current_frame_index += 1
                frames_since_last_callback += 1

                # debug.log(f"Progress: {progress_percentage}%")

                if not ret:
                    break

                abs_diff = cv2.absdiff(prev_frame, frame)
                total_difference += abs_diff.mean()

                # progress_percentage = "{:.2f}".format((current_frame_index * 100) / total_frames)
                # progress_callback(progress_percentage)

                if frames_since_last_callback == 5:
                    progress_percentage = "{:.2f}".format((current_frame_index * 100) / total_frames)
                    progress_callback(progress_percentage)
                    frames_since_last_callback = 0

                # cv2.imshow("Absolute difference", abs_diff)
                # cv2.resizeWindow("Absolute difference", 800, 600)
                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     break

                prev_frame = frame

            finished = True
            total_difference = total_difference // total_frames
            debug.log(f"Processing finished in {"{:.2f}s".format(time.time() - start_time)}", text_color="cyan")
            progress_callback("100.00")

    cap.release()
    cv2.destroyAllWindows()


def process_video_thread(path):
    global progress_callback
    if progress_callback is None:
        debug.log("Progress callback not set. Aborting video processing.", text_color="red")
        return
    thread = threading.Thread(target=process_video, args=(path, progress_callback))
    thread.start()
