import threading
import time

import numpy as np
import cv2

import debug

# Source: https://github.com/spmallick/learnopencv/blob/master/VideoStabilization/video_stabilization.py

SMOOTHING = 500
STAB_SUFFIX = "_stabilized.mp4"
progress_callback = None
is_finished = False


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


def avg_movement(curve, radius):
    window_size = 2 * radius + 1
    filt = np.ones(window_size, dtype=float) / window_size
    curve_padded = np.pad(curve, (radius, radius), mode='edge')
    curve_smoothed = np.convolve(curve_padded, filt, mode='valid')
    return curve_smoothed


def smooth(trajectory):
    # Apply moving average filter to each column of the trajectory array
    smoothed_traj = np.apply_along_axis(avg_movement, axis=0, arr=trajectory, radius=SMOOTHING)
    return smoothed_traj


def zoom_frame(frame, scale_factor=1.05):
    # Get the height and width of the frame
    height, width = frame.shape[:2]

    # Calculate the new dimensions for the content (zoomed region)
    new_width = int(width / scale_factor)
    new_height = int(height / scale_factor)

    # Calculate the top-left corner to crop the frame
    crop_x = int((width - new_width) / 2)
    crop_y = int((height - new_height) / 2)

    # Crop the frame to the zoomed region
    zoomed_region = frame[crop_y:crop_y + new_height, crop_x:crop_x + new_width]

    # Resize the zoomed region back to the original frame dimensions
    zoomed_frame = cv2.resize(zoomed_region, (width, height), interpolation=cv2.INTER_LINEAR)

    return zoomed_frame


def stabilize_video(video_path, p_callback):
    global is_finished
    # Read input video
    cap = cv2.VideoCapture(video_path)

    # Get video information
    frame_count, width, height, fps = (
        int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        cap.get(cv2.CAP_PROP_FPS)
    )

    # Define the codec for output video
    codec = cv2.VideoWriter_fourcc('F', 'F', 'V', '1')

    # Set up output video
    video_output = cv2.VideoWriter(video_path[:-4] + STAB_SUFFIX, codec, fps, (width, height))

    # Read first frame and convert it to grayscale
    _, prev_gray = cap.read()
    prev_gray = cv2.cvtColor(prev_gray, cv2.COLOR_BGR2GRAY)

    # Pre-define transformation-store array
    transforms = np.zeros((frame_count - 1, 3), np.float32)

    start_time = time.time()

    frames_since_last_callback = 0

    for i in range(frame_count + 1):
        # Detect feature points in previous frame
        prev_points = cv2.goodFeaturesToTrack(prev_gray,
                                              maxCorners=200,
                                              qualityLevel=0.2,
                                              minDistance=40,
                                              blockSize=7)

        # Read next frame
        next_frame, curr = cap.read()
        if not next_frame:
            break

        # Convert to grayscale
        curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow
        curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_points, None)

        # Sanity check
        assert prev_points.shape == curr_points.shape

        # Filter only valid points
        idx = np.where(status == 1)[0]
        prev_points = prev_points[idx]
        curr_points = curr_points[idx]

        # Find transformation matrix
        matrix = cv2.estimateAffinePartial2D(prev_points, curr_points)[0]

        # Extract translation
        dx = matrix[0, 2]
        dy = matrix[1, 2]

        # Extract rotation angle
        da = np.arctan2(matrix[1, 0], matrix[0, 0])

        # Store transformation
        transforms[i] = [dx, dy, da]

        # Move to next frame
        prev_gray = curr_gray

        print(
            f"Frame: {i}/{frame_count} - Tracked points: {len(prev_points)}" + " [{:.0f}%]".format(
                (i * 100) / frame_count))

        frames_since_last_callback += 1

        if frames_since_last_callback == 5:
            p_callback("stabilization", int("{:.0f}".format((i * 100) / frame_count)))
            frames_since_last_callback = 0

    # Calculate newer transformation array
    trajectory = np.cumsum(transforms, axis=0)
    # smoothed_trajectory = smooth(np.cumsum(transforms, axis=0))
    # difference = smooth(np.cumsum(transforms, axis=0)) - np.cumsum(transforms, axis=0)
    transforms_smooth = transforms + (smooth(trajectory) - trajectory)

    # Reset stream to first frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # Center of the first frame
    center_x, center_y = width / 2, height / 2

    # Write n_frames-1 transformed frames
    for i in range(frame_count - 2):
        next_frame, frame = cap.read()
        if not next_frame:
            break

        dx, dy, da = (
            transforms_smooth[i, 0] * 1.05,
            transforms_smooth[i, 1] * 1.05,
            transforms_smooth[i, 2] * 1.05
        )

        # Compute rotation matrix
        matrix = cv2.getRotationMatrix2D((center_x, center_y), np.degrees(da), scale=1.0)
        matrix[:, 2] += [dx, dy]

        # frame_stabilized = cv2.warpAffine(frame, matrix, (width, height))
        frame_stabilized = zoom_frame(cv2.warpAffine(frame, matrix, (width, height)), 1.2)
        video_output.write(frame_stabilized)

    # Release video
    cap.release()
    video_output.release()
    progress_callback("stabilization", 100)
    is_finished = True
    print(f"Stabilization time: {"{:.2f}s".format(time.time() - start_time)}")


def stab_video_thread(path):
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
    thread = threading.Thread(target=stabilize_video, args=(path, progress_callback))
    thread.start()
