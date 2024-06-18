import os
import numpy as np


def save_color_presets(color, lower_bound, upper_bound, base_filename="hsv_presets"):
    filename = f"{base_filename}_{color}.txt"
    with open(filename, "w") as file:
        file.write(f"LowerH {lower_bound[0]}\n")
        file.write(f"LowerS {lower_bound[1]}\n")
        file.write(f"LowerV {lower_bound[2]}\n")
        file.write(f"UpperH {upper_bound[0]}\n")
        file.write(f"UpperS {upper_bound[1]}\n")
        file.write(f"UpperV {upper_bound[2]}\n")
    print(f"{color.capitalize()} HSV values saved to {filename}")

def load_color_presets(color, base_filename="hsv_presets"):
    filename = f"{base_filename}_{color}.txt"
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            lower_bound = np.array([int(lines[0].split()[1]), int(lines[1].split()[1]), int(lines[2].split()[1])])
            upper_bound = np.array([int(lines[3].split()[1]), int(lines[4].split()[1]), int(lines[5].split()[1])])
        print(f"{color.capitalize()} HSV values loaded from {filename}")
        return lower_bound, upper_bound
    else:
        print(f"File {filename} not found. Using default values.")
        return None, None