import debug
import cv2
import numpy as np
import matplotlib.pyplot as plt


def calculate_avg_brightness(frame):
    return frame.sum() // frame.size


def plot_average_brightness(brightness_list):
    x_values = range(len(brightness_list))
    plt.figure(figsize=(16, 4))
    plt.plot(x_values, brightness_list, linestyle='-')
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title(f"Brightness visualization")
    plt.grid(True)
    plt.show()


def preprocess(path):
    cap = cv2.VideoCapture(path)

    new_path = path[:-4] + '_pass.mp4'
    ret, first_frame = cap.read()
    frame_height, frame_width = first_frame.shape[:2]

    codec = cv2.VideoWriter_fourcc(*'H264')
    output = cv2.VideoWriter(new_path, codec, 95, (frame_width, frame_height))

    curr_index = 0
    prev_frame = first_frame

    b_list = list()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_index += 1

        curr_brightness = calculate_avg_brightness(frame)
        prev_brightness = calculate_avg_brightness(prev_frame)

        b_list.append(abs(curr_brightness - prev_brightness))

        # 1 - original brightness
        if curr_brightness - prev_brightness == 0:
            delta_brightness = 1
        else:
            delta_brightness = 1 - ((curr_brightness - prev_brightness) / curr_brightness)

        print(
            f"[Frame: {curr_index}] {curr_brightness} (Difference: {curr_brightness - prev_brightness} | {delta_brightness})")
        new_frame = cv2.convertScaleAbs(frame, alpha=delta_brightness, beta=0)
        output.write(new_frame)
        # if abs(curr_brightness - prev_brightness) <= 3:
        #     output.write(frame)
        #     prev_frame = frame
        # else:
        #     ret, frame = cap.read()

    cap.release()
    output.release()

    plot_average_brightness(b_list)


preprocess('C:/sample_newly_stabilized.mp4')
# preprocess('C:/sample_newly_stabilized_pass.mp4')
# preprocess('C:/sample_newly_stabilized_pass_pass.mp4')
