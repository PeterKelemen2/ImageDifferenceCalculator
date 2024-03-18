import numpy as np
import matplotlib.pyplot as plt


def plot_average_brightness(before_list, after_list, title="Graph", path=None):
    x_values = range(len(before_list))
    plt.figure(figsize=(8, 4))
    plt.plot(x_values, before_list, linestyle='-', color='red', label="Before")
    plt.plot(x_values, after_list, linestyle='-', color='blue', label="After")
    plt.xlabel("Frame index")
    plt.ylabel("Brightness value")
    plt.title(title)
    plt.grid(True)
    plt.ylim(min(before_list) - 1, max(before_list) + 1)
    plt.xlim(0, len(x_values) - 1)
    plt.legend()
    if path:
        plt.savefig(path[:-4] + "_prepass_plot.png", dpi=150)
    plt.show()
