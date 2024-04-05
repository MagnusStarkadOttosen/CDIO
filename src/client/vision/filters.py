import cv2
import numpy as np


def apply_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("After gray")

    return gray


def apply_canny(image):
    # Compute the threshhold for the edge detection
    v = np.median(image)
    sigma = 0.33
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))

    # Edge detection
    canny = cv2.Canny(image, lower_thresh, upper_thresh, 10)
    print("After canny")
    return canny


def apply_blur(image):
    median = cv2.medianBlur(image, 5)
    print("after median")

    blurred = cv2.GaussianBlur(median, (5, 5), 0)
    print("after blurred")

    return blurred


def convert_hsv(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv


def filter_image_red(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([6, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    red_image = cv2.bitwise_and(image, image, mask=mask)

    return red_image


def filter_image_green(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_green1 = np.array([35, 70, 50])
    upper_green1 = np.array([85, 255, 255])
    lower_green2 = np.array([85, 70, 50])
    upper_green2 = np.array([92, 163, 99])

    mask1 = cv2.inRange(hsv, lower_green1, upper_green1)
    mask2 = cv2.inRange(hsv, lower_green2, upper_green2)
    mask = cv2.bitwise_or(mask1, mask2)

    green_image = cv2.bitwise_and(image, image, mask=mask)

    return green_image


def sharpen_image(image):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])

    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image


def clean_image(image):
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)

    dilated = cv2.dilate(opening, kernel, iterations=2)

    blurred = cv2.GaussianBlur(dilated, (5, 5), 0)

    return blurred


def erode_image(image, i=1):
    kernel = np.ones((4, 4), np.uint8)
    img_erosion = cv2.erode(image, kernel, iterations=i)

    return img_erosion
