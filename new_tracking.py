import cv2
import numpy as np


# Function to find offset and move the frame
def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)

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
    out = cv2.VideoWriter(output_path, codec, int(cap.get(cv2.CAP_PROP_FPS)), (frame_width, frame_height))

    curr_frame_index = 1
    while True:

        print(f"Frames: {curr_frame_index}/{total_frames}")
        # Read the current frame
        ret, frame = cap.read()

        if not ret:
            break

        # Draw the ROI rectangle on the current frame
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

        # Crop the ROI from the first frame
        template = first_frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # Use template matching to find the template in the current frame
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        # Calculate the offset with scaling factor and negate the values
        offset = (-1 * (max_loc[0] - roi_x), -1 * (max_loc[1] - roi_y))

        # Move the frame by applying the offset
        M = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
        moved_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

        # Write the processed frame to the output video file
        out.write(moved_frame)
        curr_frame_index += 1
        # Display the result
        # cv2.imshow('Moved Frame', moved_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


# Specify the path to your video file and output video file
video_path = 'C:/sample.mp4'
output_path = 'C:/sample_newly_stabilized.mp4'  # Change the file extension and path as needed

# Call the function to process the video and save the output
process_video(video_path, output_path)
