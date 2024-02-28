import time

import numpy as np
import cv2

# Source: https://github.com/spmallick/learnopencv/blob/master/VideoStabilization/video_stabilization.py

SMOOTHING = 200
STAB_SUFFIX = "_stabilized.mp4"


def avg_movement(curve, radius):
    # Compute the size of the moving average window
    window_size = 2 * radius + 1

    # Compute the filter for the moving average
    filter = np.ones(window_size, dtype=float) / window_size

    # Pad the curve with edge values
    curve_padded = np.pad(curve, (radius, radius), mode='edge')

    # Apply the convolution to compute the moving average
    curve_smoothed = np.convolve(curve_padded, filter, mode='valid')

    return curve_smoothed


def smooth(trajectory):
    # Apply moving average filter to each column of the trajectory array
    smoothed_traj = np.apply_along_axis(avg_movement, axis=0, arr=trajectory, radius=SMOOTHING)
    return smoothed_traj


def zoom_frame(frame):
    s = frame.shape
    # Add 10% scale
    t = cv2.getRotationMatrix2D((s[1] / 2, s[0] / 2), 0, 1.1)
    frame = cv2.warpAffine(frame, t, (s[1], s[0]))
    return frame


def stabilize_video(video_path):
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
    codec = cv2.VideoWriter_fourcc(*'H264')

    # Set up output video
    video_output = cv2.VideoWriter(video_path[:-4] + STAB_SUFFIX, codec, fps, (width, height))

    # Read first frame and convert it to grayscale
    _, prev_gray = cap.read()
    prev_gray = cv2.cvtColor(prev_gray, cv2.COLOR_BGR2GRAY)

    # Pre-define transformation-store array
    transforms = np.zeros((frame_count - 1, 3), np.float32)

    start_time = time.time()

    for i in range(frame_count + 1):
        # Detect feature points in previous frame
        prev_points = cv2.goodFeaturesToTrack(prev_gray,
                                              maxCorners=200,
                                              qualityLevel=0.1,
                                              minDistance=30,
                                              blockSize=10)

        # Read next frame
        next_frame, curr = cap.read()
        if not next_frame:
            break

        # Convert to grayscale
        curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow
        curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_points, None, maxLevel=2)

        # Sanity check
        assert prev_points.shape == curr_points.shape

        # Filter only valid points
        idx = np.where(status == 1)[0]
        prev_points = prev_points[idx]
        curr_points = curr_points[idx]

        # Find transformation matrix
        matrix = cv2.estimateAffinePartial2D(prev_points, curr_points)[0]  # will only work with OpenCV-3 or less

        # Extract traslation
        dx = matrix[0, 2]
        dy = matrix[1, 2]

        # Extract rotation angle
        da = np.arctan2(matrix[1, 0], matrix[0, 0])

        # Store transformation
        transforms[i] = [dx, dy, da]

        # Move to next frame
        prev_gray = curr_gray

        print(f"Frame: {i}/{frame_count} - Tracked points: {len(prev_points)}")

    # Calculate newer transformation array
    transforms_smooth = transforms + (smooth(np.cumsum(transforms, axis=0)) - np.cumsum(transforms, axis=0))

    # Reset stream to first frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Write n_frames-1 transformed frames
    for i in range(frame_count - 2):
        # Read next frame
        next_frame, frame = cap.read()
        if not next_frame:
            break

        dx, dy, da = (
            transforms_smooth[i, 0],
            transforms_smooth[i, 1],
            transforms_smooth[i, 2]
        )

        # Compute rotation matrix
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), np.degrees(da), scale=1.0)
        matrix[:, 2] += [dx, dy]

        # Apply affine wrapping to the given frame
        frame_stabilized = cv2.warpAffine(frame, matrix, (width, height))

        # Fix border artifacts
        # frame_stabilized = zoom_frame(frame_stabilized)

        # Write the frame to the file
        video_output.write(frame_stabilized)

    # Release video
    cap.release()
    video_output.release()

    print(f"Stabilization time: {"{:.2f}s".format(time.time() - start_time)}")
