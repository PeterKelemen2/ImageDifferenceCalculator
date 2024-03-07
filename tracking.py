import cv2
import numpy as np

def stabilize_video(input_path, output_path):
    # Open the video file
    cap = cv2.VideoCapture(input_path)

    # Read the first frame
    ret, prev_frame = cap.read()

    # Convert the first frame to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Detect AKAZE keypoints and descriptors in the first frame
    akaze = cv2.AKAZE_create()
    keypoints1, descriptors1 = akaze.detectAndCompute(prev_gray, None)

    # Create a VideoWriter object for the stabilized output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (prev_frame.shape[1], prev_frame.shape[0]))

    while True:
        print(f"Processing {cap.get(cv2.CAP_PROP_POS_FRAMES)}/{cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
        # Read the next frame
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the current frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AKAZE keypoints and descriptors in the current frame
        keypoints2, descriptors2 = akaze.detectAndCompute(gray, None)

        # Use the BFMatcher to find the best matches between descriptors
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)

        # Adjust the threshold for the ratio test
        good_matches = [m for m, n in matches if m.distance < 0.6 * n.distance]

        # Estimate the homography matrix using the good matches
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Adjust the RANSAC threshold
        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1.0)

        # Warp the frame based on the homography matrix
        stabilized_frame = cv2.warpPerspective(frame, H, (frame.shape[1], frame.shape[0]))

        # Write the stabilized frame to the output video
        out.write(stabilized_frame)

        # Set the current frame as the previous frame for the next iteration
        prev_gray = gray.copy()
        keypoints1 = keypoints2
        descriptors1 = descriptors2

    # Release video capture and writer objects
    cap.release()
    out.release()

    # Destroy any OpenCV windows
    cv2.destroyAllWindows()

# print(f"Processing {cap.get(cv2.CAP_PROP_POS_FRAMES)}/{cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
# Example usage
input_video_path = 'C:/sample.mp4'
output_video_path = 'C:/experimental.avi'
stabilize_video(input_video_path, output_video_path)
