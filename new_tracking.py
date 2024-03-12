import cv2
import numpy as np


# Function to find offset and move the frame
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, first_frame = cap.read()

    # Select a region of interest (ROI) in the first frame
    roi = cv2.selectROI(first_frame)
    cv2.destroyAllWindows()

    # Set a scaling factor to control the movement distance
    scaling_factor = 1.0

    while True:
        # Read the current frame
        ret, frame = cap.read()

        if not ret:
            break

        # Draw the ROI rectangle on the current frame
        cv2.rectangle(frame, (int(roi[0]), int(roi[1])), (int(roi[0] + roi[2]), int(roi[1] + roi[3])), (0, 255, 0), 2)

        # Crop the ROI from the first frame
        template = first_frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

        # Use template matching to find the template in the current frame
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        # Calculate the offset with scaling factor and negate the values
        offset = (-scaling_factor * (max_loc[0] - roi[0]), -scaling_factor * (max_loc[1] - roi[1]))

        # Move the frame by applying the offset
        M = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
        moved_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

        # Display the result
        cv2.imshow('Moved Frame', moved_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Specify the path to your video file
video_path = 'C:/sample.mp4'

# Call the function to process the video
process_video(video_path)
