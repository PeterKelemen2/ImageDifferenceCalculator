import cv2

import debug
import interface

progress_callback = None


def set_progress_callback(callback):
    global progress_callback
    progress_callback = callback


def process_video(path):
    current_frame_index = 0
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
                progress_percentage = int("{:.0f}".format((current_frame_index * 100) / total_frames))

                debug.log(f"Progress: {progress_percentage}%")

                # interface.Interface.update_progress_bar(progress_percentage)

                if not ret:
                    break

                abs_diff = cv2.absdiff(prev_frame, frame)
                cv2.imshow("Absolute difference", abs_diff)
                cv2.resizeWindow("Absolute difference", 800, 600)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

                prev_frame = frame

    cap.release()
    cv2.destroyAllWindows()