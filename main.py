import random
import subprocess
import time

import matplotlib.pyplot as plt
import numpy as np
import os
import math
import imageio.v2 as imageio
import shutil

import pygetwindow


class TextColors:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def quicksort(lower_bound, upper_bound):
    global global_number_list, comparison_count, swap_count

    if lower_bound < upper_bound:
        number_list = global_number_list[lower_bound:upper_bound + 1]
        pivot = number_list[-1]
        first_half = []
        second_half = []

        for i in range(len(number_list) - 1):
            comparison_count += 1
            if number_list[i] <= pivot:
                first_half.append(number_list[i])
            else:
                second_half.append(number_list[i])

        global_number_list[lower_bound:upper_bound + 1] = first_half + [pivot] + second_half
        swap_count += 1

        pivot_index = lower_bound + len(first_half)
        draw_bar_graph(global_number_list, pivot_index)

        quicksort(lower_bound, pivot_index - 1)
        quicksort(pivot_index + 1, upper_bound)


def bubblesort():
    global global_number_list, comparison_count, swap_count
    for i in range(len(global_number_list)):
        for j in range(0, len(global_number_list) - 1 - i):
            if global_number_list[j] > global_number_list[j + 1]:
                temp = global_number_list[j]
                global_number_list[j] = global_number_list[j + 1]
                global_number_list[j + 1] = temp
                swap_count += 1
            comparison_count += 1
            draw_bar_graph(global_number_list, j)


def draw_bar_graph(arr, highlighted_element):
    global plot_counter
    x = np.arange(len(arr))
    colors = ['blue'] * len(arr)
    colors[highlighted_element] = 'red'

    plt.figure(figsize=(20, 10), dpi=150)
    plt.bar(x, arr, color=colors)
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Elements of the Array")
    plot_filename = os.path.join(plot_directory, f"plot_{plot_counter:03d}.png")
    plt.savefig(plot_filename)
    plt.close()
    plot_counter += 1


n = int(input(f"{TextColors.GREEN}Enter the desired number of elements: {TextColors.RESET}"))

global_number_list = [None] * n

for i in range(n):
    global_number_list[i] = random.randint(1, n)
print(f"{TextColors.YELLOW}{global_number_list}{TextColors.RESET}")

render_directory = os.getcwd() + "\\visual render of sorting"
plot_directory = render_directory + "\\plots"
gif_directory = render_directory + "\\gif"

try:
    shutil.rmtree(render_directory)
except Exception as e:
    print(f"Failed to delete '{render_directory}'. Reason: {e}")

os.makedirs(render_directory)
os.makedirs(plot_directory)
os.makedirs(gif_directory)

plot_counter = 0
comparison_count = 0

swap_count = 0

draw_bar_graph(global_number_list, len(global_number_list) - 1)

match input(f"{TextColors.GREEN}enter the sorting algorithm [quick sort, bubble sort]: {TextColors.RESET}"):
    case "bubble sort" | "bubblesort":
        print(
            f"{TextColors.CYAN}sorting using bubble sort, creating plots and saving them as images...{TextColors.RESET}")
        bubblesort()

        theoretical_operations = n ** 2

        print(f"{TextColors.YELLOW}        <--------TECHNICAL INFO-------->")
        print(global_number_list)
        print(f"Total comparisons: {comparison_count}")
        print(f"Total swaps: {swap_count}")
        print(f"Theoretical operations (O(n^2)): {theoretical_operations:.0f}")
        print(f"{TextColors.YELLOW}        <-------/TECHNICAL INFO-------->{TextColors.RESET}")

    case "quick sort" | "quicksort":
        print(
            f"{TextColors.CYAN}sorting using quick sort, creating plots and saving them as images...{TextColors.RESET}")
        quicksort(0, len(global_number_list) - 1)
        theoretical_operations = n * math.log2(n)

        print(f"{TextColors.YELLOW}        <--------TECHNICAL INFO-------->")
        print(global_number_list)
        print(f"Total comparisons: {comparison_count}")
        print(f"Total swaps: {swap_count}")
        print(f"Theoretical operations (O(n log(n))): {theoretical_operations:.0f}")
        print(f"{TextColors.YELLOW}        <-------/TECHNICAL INFO-------->{TextColors.RESET}")

    case _:
        print("wrong input")
        exit()

fig, ax = plt.subplots()


def update(frame):
    img = plt.imread(frame)
    ax.imshow(img)
    ax.axis('off')


plot_filenames = sorted(
    [os.path.join(plot_directory, fname) for fname in os.listdir(plot_directory) if fname.endswith('.png')])

images = []

print(f"{TextColors.CYAN}rendering gif from plot images...{TextColors.RESET}")

for filename in plot_filenames:
    images.append(imageio.imread(filename))
imageio.mimsave(gif_directory + '\\animation_of_plots.gif', images)

print(f"{TextColors.BOLD}{TextColors.CYAN}done! opening the render directory")
try:
    os.startfile(render_directory)
    print("opened in file explorer")
except Exception as e:
    print(f"Failed to open the render directory. Reason: {e}")
    print(
        f"{render_directory}{TextColors.RESET}")