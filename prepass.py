import time

import debug
import cv2
import numpy as np
import matplotlib.pyplot as plt


def calculate_avg_brightness(frame):
    # return frame.sum() // frame.size
    return np.mean(frame)


def print_as_table_row(i, curr, first, delta):
    # print(
    #     f"[{i}] {curr} (Difference: {curr - first} | {delta})")

    index_space = 4 - len(str(i))
    curr_space = 22 - len(str(curr))
    diff_space = 22 - len(str(curr - first))
    delta_space = 6 - len(str(delta))

    line = (" " * index_space + str(i) +
            " | " + " " * curr_space + str(curr) +
            " | " + " " * diff_space + str(curr - first) +
            " | " + " " * delta_space + str(delta))
    print(line)


def plot_average_brightness(before_list, after_list, title="Graph", path=None):
    x_values = np.arange(len(before_list))
    # x_values = range(len(before_list))
    plt.figure(figsize=(8, 4))
    plt.plot(x_values, before_list, linestyle='-', color='red', label="Before")
    plt.plot(x_values, after_list, linestyle='-', color='blue', label="After")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title(title)
    plt.grid(True)
    plt.ylim(min(before_list) - 1, max(before_list) + 1)
    plt.xlim(0, len(x_values) - 1)
    plt.legend()
    if path:
        plt.savefig(path[:-4] + "_prepass_plot.png", dpi=150)
    plt.show()


def preprocess(path, to_plot=True):
    start_time = time.time()

    cap = cv2.VideoCapture(path)

    new_path = path[:-4] + '_prepass.mp4'
    ret, first_frame = cap.read()
    frame_height, frame_width = first_frame.shape[:2]

    codec = cv2.VideoWriter_fourcc(*'H264')
    output = cv2.VideoWriter(new_path, codec, 95, (frame_width, frame_height))

    curr_index = 0
    first_frame_brightness = calculate_avg_brightness(first_frame)

    b_list, prepass_b_list = [], []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        curr_index += 1

        curr_brightness = calculate_avg_brightness(frame)
        b_list.append(curr_brightness)

        delta_brightness = 1 - ((curr_brightness - first_frame_brightness) / curr_brightness)
        # delta_brightness = round(1 - ((curr_brightness - first_frame_brightness) / curr_brightness), 4)
        if curr_brightness - first_frame_brightness == 0:
            delta_brightness = 1

        print_as_table_row(curr_index, curr_brightness, first_frame_brightness, delta_brightness)

        frame = cv2.convertScaleAbs(frame, alpha=delta_brightness, beta=0)
        prepass_b_list.append(calculate_avg_brightness(frame))

        output.write(frame)

    cap.release()
    output.release()
    if to_plot:
        plot_average_brightness(before_list=b_list, after_list=prepass_b_list, title="Brightness regulation", path=path)
    debug.log(f"Prepass finished in {"{:.2f}s".format(time.time() - start_time)}", text_color="cyan")


preprocess('C:/sample_newly_stabilized.mp4', to_plot=True)
