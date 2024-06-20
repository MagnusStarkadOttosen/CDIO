import math
import logging

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


def get_distance(current_pos, target_pos):
    print(f"current pos :  {current_pos} and target_pos :  {target_pos}")
    dist_vector = current_pos - target_pos
    distance = round(math.sqrt(dist_vector[0] ** 2 + dist_vector[1] ** 2), 1)
    return distance


# Configure the first logger
logger1 = logging.getLogger('safe_detect_balls')
logger1.setLevel(logging.DEBUG)
file_handler1 = logging.FileHandler('safe_detect_balls.log')
file_handler1.setLevel(logging.DEBUG)
formatter1 = logging.Formatter('%(asctime)s - %(message)s')
file_handler1.setFormatter(formatter1)
logger1.addHandler(file_handler1)

# Configure the second logger
logger2 = logging.getLogger('buffered_path')
logger2.setLevel(logging.DEBUG)
file_handler2 = logging.FileHandler('buffered_path.log')
file_handler2.setLevel(logging.DEBUG)
formatter2 = logging.Formatter('%(asctime)s - %(message)s')
file_handler2.setFormatter(formatter2)
logger2.addHandler(file_handler2)


def log_balls(message):
    logger1.debug(message)


def log_path(message):
    logger2.info(message)
