import threading

import cv2
import numpy as np

import debug
import plotting

progress_callback = None
is_finished = False
stab_thread = None


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
def stabilize_video(video_path, p_callback=None):
    global is_finished

    # Read video input
    cap = cv2.VideoCapture(video_path)
    cv2.setNumThreads(2)
    output = video_path[:-4] + "_stabilized.mp4"

    # Read the first frame
    ret, first_frame = cap.read()

    # Get the dimensions of the first frame
    frame_height, frame_width = first_frame.shape[:2]
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the position and dimensions of the ROI
    roi_width, roi_height = frame_width // 4, frame_height // 4
    roi_x = (frame_width - roi_width) // 2
    roi_y = (frame_height - roi_height) // 2

    # Define the output video codec and create a VideoWriter object
    codec = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter(output, codec, int(cap.get(cv2.CAP_PROP_FPS)), (frame_width, frame_height))

    curr_frame_index = 1
    movement_data = []

    while True:
        print(f"Frames: {curr_frame_index}/{total_frames}")

        if (curr_frame_index % 10) % 5 == 0 and p_callback is not None:
            p_callback("stabilization", int("{:.0f}".format((curr_frame_index * 100) / total_frames)))

        # Read the current frame
        ret, frame = cap.read()

        if not ret:
            break

        # Draw the ROI rectangle on the current frame
        # cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

        # Crop the ROI from the first frame
        template = first_frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # Use template matching to find the template in the current frame
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        # Calculate the offset with scaling factor and negate the values
        offset = (-1 * (max_loc[0] - roi_x), -1 * (max_loc[1] - roi_y))
        movement_data.append(offset)
        # Move the frame by applying the offset
        M = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
        moved_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

        # Write the processed frame to the output video file
        out.write(moved_frame)
        curr_frame_index += 1

    cap.release()
    out.release()
    # cv2.destroyAllWindows()
    if p_callback is not None:
        progress_callback("stabilization", 100)
    is_finished = True
    plotting.plot_stabilization_movement(movement_data=movement_data,
                                         title="Stabilization movement",
                                         path=video_path[:-4] + "stabilization_plot.png")


def stab_video_thread(path):
    """
    Creates a thread for video processing.

    This function creates a separate thread to process the video specified by `path`.

    Parameters:
        path (str): The path to the video file.
    """
    global progress_callback, stab_thread
    if progress_callback is None:
        debug.log("Progress callback not set. Aborting video processing.", text_color="red")
        return
    stab_thread = threading.Thread(target=stabilize_video, args=(path, progress_callback))
    stab_thread.start()
