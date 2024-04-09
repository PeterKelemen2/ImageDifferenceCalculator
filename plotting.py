import numpy as np
import matplotlib.pyplot as plt


def plot_average_brightness(before_list, after_list, title="Fényerő normalizálás", size=(8, 4), path=None, dpi=150):
    x_values = range(len(before_list))
    plt.figure(figsize=size)
    plt.plot(x_values, before_list, linestyle='-', color='red', label="Előtte")
    plt.plot(x_values, after_list, linestyle='-', color='blue', label="Utána")
    plt.xlabel("Képkocka index")
    plt.ylabel("Fényerő érték")
    plt.title(title)
    plt.grid(True)
    plt.ylim(min(before_list) - 1, max(before_list) + 1)
    plt.xlim(0, len(x_values) - 1)
    plt.legend()
    if path:
        plt.savefig(path[:-4] + "_prepass_plot.png", dpi=dpi)
    plt.show()


def plot_stabilization_movement(movement_data, title="Mozgás stabilizálása", size=(8, 4), path=None, dpi=150):
    avg_movement = [(item[0] + item[1]) / 2 for item in movement_data]
    index = range(len(avg_movement))
    plt.figure(figsize=size)
    plt.plot(index, avg_movement, linestyle='-', label="Átlagos mozgás")
    plt.xlabel("Képkocka index")
    plt.ylabel("Mozgás mértéke")
    plt.title(title)
    plt.grid(True)
    plt.ylim(min(avg_movement) - 1, max(avg_movement) + 1)
    plt.xlim(0, len(index) - 1)
    plt.legend()
    if path:
        plt.savefig(path[:-4] + "_stabilization_plot.png", dpi=dpi)
    plt.show()
