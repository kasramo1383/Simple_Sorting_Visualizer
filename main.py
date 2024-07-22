# region Modules
import random
import matplotlib.pyplot as plt
import numpy as np
import os
import math

import imageio.v2 as imageio

import shutil
from pydub import AudioSegment
from pydub.generators import Sine

from proglog import TqdmProgressBarLogger
from moviepy.editor import VideoFileClip, AudioFileClip


# endregion

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


# region Variables
melody = AudioSegment.silent(duration=0)

n = int(input(f"{TextColors.GREEN}Enter the desired number of elements: {TextColors.RESET}"))

global_number_list = [i for i in range(1, n + 1)]

render_directory = os.getcwd() + "\\visual render of sorting"
plot_directory = render_directory + "\\plots"

plot_counter = 0
comparison_count = 0

swap_count = 0


# endregion
# region Sorting Methods
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
        number_to_frequency_and_add_tone(pivot, n)

        quicksort(lower_bound, pivot_index - 1)
        quicksort(pivot_index + 1, upper_bound)


def bubblesort():
    global global_number_list, comparison_count, swap_count
    for i in range(len(global_number_list)):
        for j in range(0, len(global_number_list) - 1 - i):
            held = global_number_list[j]
            compared = global_number_list[j + 1]
            if held > compared:
                temp = global_number_list[j]
                global_number_list[j] = compared
                global_number_list[j + 1] = temp
                swap_count += 1

            comparison_count += 1
            draw_bar_graph(global_number_list, j)
            number_to_frequency_and_add_tone(held, n)


# endregion
# region Other Methods
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


def number_to_frequency_and_add_tone(number, max_number):
    global melody
    min_freq = 220  # A3 note
    max_freq = 880  # A5 note
    frequency = min_freq + (max_freq - min_freq) * (number - 1) / (max_number - 1)
    tone = generate_tone(frequency)
    melody += tone


def generate_tone(frequency, duration=100):
    return Sine(frequency).to_audio_segment(duration=duration)


def update(frame):
    img = plt.imread(frame)
    ax.imshow(img)
    ax.axis('off')


# endregion

random.shuffle(global_number_list)

print(f"{TextColors.YELLOW}{global_number_list}{TextColors.RESET}")

try:
    shutil.rmtree(render_directory)
except Exception as e:
    print(f"Failed to delete '{render_directory}'. Reason: {e}")

os.makedirs(render_directory)
os.makedirs(plot_directory)

draw_bar_graph(global_number_list, len(global_number_list) - 1)

# region Sorting Algorithm match case
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
# endregion

fig, ax = plt.subplots()

# region rendering
plot_filenames = sorted(
    [os.path.join(plot_directory, fname) for fname in os.listdir(plot_directory) if fname.endswith('.png')])

images = []

print(f"{TextColors.CYAN}rendering gif from plot images...{TextColors.RESET}")

for filename in plot_filenames:
    images.append(imageio.imread(filename))
imageio.mimsave(render_directory + '\\animation_of_plots.gif', images)



print(f"{TextColors.CYAN}exporting audio file...{TextColors.RESET}")
melody.export(render_directory + "\\melody.wav", format="wav")


print(f"{TextColors.CYAN}creating video...{TextColors.RESET}")

gif_clip = VideoFileClip(render_directory + "\\animation_of_plots.gif")
audio_clip = AudioFileClip(render_directory + "\\melody.wav")

gif_clip = gif_clip.set_duration(max(gif_clip.duration, audio_clip.duration) + 2)

video_with_audio = gif_clip.set_audio(audio_clip)

progress_logger = TqdmProgressBarLogger(bars=['main'],print_messages=False,notebook=False)
video_with_audio.write_videofile(render_directory + "\\output_video.mp4", codec="libx264", audio_codec="aac", logger=progress_logger)


print(f"{TextColors.BOLD}{TextColors.CYAN}done! opening the render directory")
try:
    os.startfile(render_directory)
    print("opened in file explorer")
except Exception as e:
    print(f"Failed to open the render directory. Reason: {e}")
    print(
        f"{render_directory}{TextColors.RESET}")
# endregion
