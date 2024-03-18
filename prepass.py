import debug
import cv2
import numpy as np
import matplotlib.pyplot as plt


def calculate_avg_brightness(frame):
    return frame.sum() // frame.size


def plot_average_brightness(before_list, after_list, title="Average", path=None):
    x_values = range(len(before_list))
    plt.figure(figsize=(10, 4))
    plt.plot(x_values, before_list, linestyle='-', color='red', label="Before")
    plt.plot(x_values, after_list, linestyle='-', color='blue', label="After")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title(title)
    plt.grid(True)
    plt.ylim(min(before_list) - 1, max(before_list) + 1)
    plt.legend()
    if path:
        plt.savefig(path[:-4] + "_prepass_plot.png", dpi=150)
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
    prepass_b_list = list()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_index += 1

        curr_brightness = calculate_avg_brightness(frame)
        prev_brightness = calculate_avg_brightness(prev_frame)

        b_list.append(curr_brightness)

        delta_brightness = 1 - ((curr_brightness - prev_brightness) / curr_brightness)
        if curr_brightness - prev_brightness == 0:  # or delta_brightness > 1.005:
            delta_brightness = 1

        print(
            f"[Frame: {curr_index}] {curr_brightness} (Difference: {curr_brightness - prev_brightness} | {delta_brightness})")
        frame = cv2.convertScaleAbs(frame, alpha=delta_brightness, beta=0)

        prepass_b_list.append(calculate_avg_brightness(frame))

        output.write(frame)

        # prev_frame = frame

    cap.release()
    output.release()

    plot_average_brightness(before_list=b_list, after_list=prepass_b_list, title="Before regulation", path=path)


preprocess('C:/sample_newly_stabilized.mp4')
# preprocess('C:/sample_newly_stabilized_pass.mp4')
# preprocess('C:/sample_newly_stabilized_pass_pass.mp4')
