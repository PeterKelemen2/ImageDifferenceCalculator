import numpy as np
import matplotlib.pyplot as plt


def plot_average_brightness(before_list, after_list, title="Graph", path=None):
    x_values = range(len(before_list))
    plt.figure(figsize=(8, 4))
    plt.plot(x_values, before_list, linestyle='-', color='red')
    plt.plot(x_values, after_list, linestyle='-', color='blue')
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


def plot(values: list, title="Graph", graph_labels=None, legend_labels=None, size=(8, 4), path=None, dpi=150):
    plt.figure(figsize=size)

    if values:
        if len(values) > 1:
            x_values = range(len(max(values)))
            i = 0
            for value in values:
                if legend_labels:
                    label = legend_labels[i]
                    plt.plot(x_values, value, linestyle='-', label=label)
                else:
                    plt.plot(x_values, value, linestyle='-')
                i += 1
        else:
            x_values = range(len(values[0]))
            plt.plot(x_values, values[0], linestyle='-')

    min_value, max_value = 255, 0

    for value in values:
        for elem in value:
            if elem < min_value:
                min_value = elem
            elif elem > max_value:
                max_value = elem

    if graph_labels and len(graph_labels) > 1:
        plt.xlabel(graph_labels[0])
        plt.ylabel(graph_labels[1])

    plt.title(title)
    plt.grid(True)
    plt.ylim(min_value - 1, max_value + 1)
    if x_values:
        plt.xlim(0, len(x_values) - 1)

    plt.legend()
    if path:
        plt.savefig(path[:-4] + "_prepass_plot.png", dpi=dpi)
    plt.show()
