import random
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import imageio.v2 as imageio
import shutil

n = int(input("Enter number of elements: "))

global_number_list = [None] * n

for i in range(n):
    global_number_list[i] = random.randint(1, 200)

plot_dir = "plots"
try:
    shutil.rmtree(plot_dir)
except Exception as e:
    print(f"Failed to delete '{plot_dir}'. Reason: {e}")

os.makedirs(plot_dir)

plot_counter = 0

comparison_count = 0
swap_count = 0


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


def draw_bar_graph(arr, pivot_index):
    global plot_counter
    x = np.arange(len(arr))
    colors = ['blue'] * len(arr)
    colors[pivot_index] = 'red'

    plt.figure(figsize=(20, 10), dpi=150)
    plt.bar(x, arr, color=colors)
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Elements of the Array")
    plot_filename = os.path.join(plot_dir, f"plot_{plot_counter:03d}.png")
    plt.savefig(plot_filename)
    plt.close()
    plot_counter += 1


draw_bar_graph(global_number_list, len(global_number_list) - 1)

match input("enter the sorting algorithm: "):
    case "bubble sort" | "bubblesort":
        bubblesort()

        theoretical_operations = n ** 2

        print(global_number_list)
        print(f"Total comparisons: {comparison_count}")
        print(f"Total swaps: {swap_count}")
        print(f"Theoretical operations (O(n^2)): {theoretical_operations:.0f}")

    case "quick sort" | "quicksort":
        quicksort(0, len(global_number_list) - 1)

        theoretical_operations = n * math.log2(n)

        print(global_number_list)
        print(f"Total comparisons: {comparison_count}")
        print(f"Total swaps: {swap_count}")
        print(f"Theoretical operations (O(n log n)): {theoretical_operations:.0f}")

    case _:
        print("wrong input")
        exit()

fig, ax = plt.subplots()


def update(frame):
    img = plt.imread(frame)
    ax.imshow(img)
    ax.axis('off')


plot_filenames = sorted([os.path.join(plot_dir, fname) for fname in os.listdir(plot_dir) if fname.endswith('.png')])

images = []

gif_dir = "gif"

try:
    shutil.rmtree(gif_dir)
except Exception as e:
    print(f"Failed to delete '{gif_dir}'. Reason: {e}")

os.makedirs(gif_dir)

for filename in plot_filenames:
    images.append(imageio.imread(filename))
imageio.mimsave(gif_dir + '\\plot_animation.gif', images)
