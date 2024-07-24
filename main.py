import random
import matplotlib.pyplot as plt
import numpy as np
import os
import math

import imageio.v2 as imageio

import shutil

from matplotlib.ticker import MaxNLocator
from moviepy.video.compositing.concatenate import concatenate_videoclips
from pydub import AudioSegment
from pydub.generators import Sine

from proglog import TqdmProgressBarLogger
from moviepy.editor import VideoFileClip, AudioFileClip


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
batch_gif_directory = render_directory + "\\batch gifs"

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

        pivot_index = lower_bound + len(first_half)
        draw_bar_graph(pivot_index)
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
            draw_bar_graph(j)
            number_to_frequency_and_add_tone(compared, n)


# endregion
# region Other Methods
def draw_bar_graph(highlighted_element):
    global plot_counter
    x = np.arange(len(global_number_list))
    colors = ['blue'] * len(global_number_list)
    colors[highlighted_element] = 'red'

    plt.figure(figsize=(20, 10), dpi=150)
    plt.bar(x, global_number_list, color=colors)

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    plot_filename = os.path.join(plot_directory, f"plot_{plot_counter:03d}.png")
    plt.savefig(plot_filename, bbox_inches='tight')
    plt.close()

    plot_counter += 1


def draw_final_bar_graphs():
    global plot_counter
    colors = ['gray'] * len(global_number_list)
    for i in range(len(global_number_list)):
        x = np.arange(len(global_number_list))
        colors[i] = 'green'

        plt.figure(figsize=(20, 10), dpi=150)
        plt.bar(x, global_number_list, color=colors)

        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()
        plot_filename = os.path.join(plot_directory, f"plot_{plot_counter:03d}.png")
        plt.savefig(plot_filename, bbox_inches='tight')
        plt.close()
        plot_counter += 1


def number_to_frequency_and_add_tone(number, max_number):
    global melody
    min_freq = 200
    max_freq = 500
    frequency = min_freq + (max_freq - min_freq) * (number - 1) / (max_number - 1)
    tone = generate_tone(frequency)
    melody += tone


def all_number_to_frequency_and_add_tone():
    for element in global_number_list:
        number_to_frequency_and_add_tone(element, n)


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
os.makedirs(batch_gif_directory)

# region Sorting Algorithm match case
match input(f"{TextColors.GREEN}enter the sorting algorithm [quick sort, bubble sort]: {TextColors.RESET}"):
    case "bubble sort" | "bubblesort":
        draw_bar_graph(0)

        print(
            f"{TextColors.CYAN}sorting using bubble sort, creating plots and saving them as images...{TextColors.RESET}")
        bubblesort()

        theoretical_operations = n ** 2

        print(f"{TextColors.YELLOW}        <--------TECHNICAL INFO-------->\n")
        print(global_number_list)
        print(f"Total comparisons: {comparison_count}")
        print(f"Total swaps: {swap_count}")
        print(f"Theoretical operations (O(n^2)): {theoretical_operations:.0f}")
        print(f"\n{TextColors.YELLOW}        <-------/TECHNICAL INFO-------->{TextColors.RESET}")

    case "quick sort" | "quicksort":
        draw_bar_graph(len(global_number_list) - 1)

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
print(f"{TextColors.CYAN}rendering the final state of the array...{TextColors.RESET}")
draw_final_bar_graphs()
all_number_to_frequency_and_add_tone()

print(f"{TextColors.CYAN}creating gif from plot images...{TextColors.RESET}")
plot_filenames = sorted(
    [os.path.join(plot_directory, frame_name) for frame_name in os.listdir(plot_directory) if
     frame_name.endswith('.png')])

batch_size = 100  # it takes up too much memory lol
batch_counter = 0
print(
    f"{TextColors.YELLOW}{plot_counter} plots. Seperated into {math.ceil(plot_counter / batch_size)} batches{TextColors.RESET}")
batches = [plot_filenames[i:i + batch_size] for i in range(0, len(plot_filenames), batch_size)]
clips = []  # for concatenating all gifs

for batch in batches:
    batch_counter += 1
    print(f"{TextColors.CYAN}{TextColors.UNDERLINE}started batch {batch_counter}...{TextColors.RESET}")
    batch_images = [imageio.imread(frame_name) for frame_name in batch]
    imageio.mimsave(os.path.join(batch_gif_directory, f"batch_gif_{batch_counter:03d}.gif"), batch_images)
    del batch_images
    clips.append(VideoFileClip(batch_gif_directory + f"\\batch_gif_{batch_counter:03d}.gif"))

print(f"{TextColors.CYAN}creating audio file...{TextColors.RESET}")
melody.export(render_directory + "\\melody.wav", format="wav")

print(f"{TextColors.CYAN}creating video...{TextColors.RESET}")

clips[-1] = clips[-1].set_duration(clips[-1].duration + 2)
gif_clip = concatenate_videoclips(clips, method="compose")
audio_clip = AudioFileClip(render_directory + "\\melody.wav")

gif_clip = gif_clip.set_duration(max(gif_clip.duration, audio_clip.duration))

video_with_audio = gif_clip.set_audio(audio_clip)

progress_logger = TqdmProgressBarLogger(bars=['main'], print_messages=False, notebook=False)
video_with_audio.write_videofile(render_directory + "\\output_video.mp4", codec="libx264", audio_codec="aac",
                                 logger=progress_logger)

print(f"{TextColors.BOLD}{TextColors.CYAN}done! opening the render directory")
try:
    os.startfile(render_directory)
    print("opened in file explorer")
except Exception as e:
    print(f"Failed to open the render directory. Reason: {e}")
    print(
        f"{render_directory}{TextColors.RESET}")
# endregion
