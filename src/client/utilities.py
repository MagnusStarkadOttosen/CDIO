import math

DPI = 96  # RESOLUTION


def convert_px_to_cm(pixel_value): # TODO: Should this one be kept, or convert_px_cm_temp?
    return pixel_value / 10


def convert_px_cm_temp(width_px, height_px): # TODO: Should this one be kept, or convert_px_cm?
    width_in, height_in = convert_px_to_inches(width_px, height_px)
    return width_in * 2.54, height_in * 2.54


def convert_px_to_inches(width_px, height_px):
    width_in = width_px / DPI
    height_in = height_px / DPI
    return width_in, height_in


def get_distance(robot_pos, target_pos):
    print(f"robot pos :  {robot_pos} and target_pos :  {target_pos}")
    dist_vector = robot_pos - target_pos
    distance = round(math.sqrt(dist_vector[0] ** 2 + dist_vector[1] ** 2), 1)
    return distance
