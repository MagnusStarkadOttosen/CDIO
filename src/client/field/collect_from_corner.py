
import math

import numpy as np

from src.client.field.navigate_to_target import *
from src.client.vision.shape_detection import detect_balls
from testing.visualization import draw_circles, get_ball_coordinates

# from src.client.pc_client import ClientPC


target_point = (300, 600)
#turn_angle = 75
CORNERS = {(0, 0), (0,1200), (1800,0), (1800,1200)}
PIVOT_POINTS = {(300,600), (1500,600)}
# client_pc = ClientPC()


def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)


def collect_from_corner(client_pc, camera):
    # Take initial image
    capture_image(camera, "test.jpg")
    image = cv2.imread("images/capturedImage/test.jpg")
    # Find corners
    #corner_point = find_corner_points_full(image)


    #dist=calculate_distance(corner_point, target_point)
    print("test1")
    client_pc.send_command("start_collect")
    navigate_to_target(CORNERS, camera, client_pc, target_point)
    print("test2")
    capture_image(camera, "test1.jpg")
    image = cv2.imread("images/capturedImage/test1.jpg")
    dst_size = (1200, 1800)
    gen_warped_image = warp_perspective(image, CORNERS, dst_size)
    robot_pos, robot_direction = detect_robot(gen_warped_image)
    print("testing testing")
    # turn_angle =  rotate_vector_to_point(robot_pos, robot_direction, corner_point)
    # client_pc.send_command(f"turn {turn_angle}")
    # print("I am in deliver point")

    #navigate_robot_to_target(target_point, camera, client_pc,corner_point)

    # client_pc.send_command("start_drive")
    # client_pc.send_command(f"drive_backwards {dist}")
    # client_pc.send_command(f"turn {-turn_angle}")
    client_pc.send_command("stop")


def check_corners(circles, image_size, threshold=50):
    corners = {
        "top_left": (0, 0),
        "top_right": (image_size[1], 0),
        "bottom_left": (0, image_size[0]),
        "bottom_right": (image_size[1], image_size[0])
    }

    for x, y, radius in circles:
        if np.linalg.norm(np.array([x, y]) - np.array(corners["top_left"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the top-left corner.")
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["top_right"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the top-right corner.")
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_left"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the bottom-left corner.")
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_right"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the bottom-right corner.")


def get_ball_coordinates(camera, corner_threshold=50):
    # Load the image
    image = cv2.imread(camera)

    if image is None:
        print(f"Error: Unable to read image from camera {camera}")
        return []

    # Get image size
    image_size = image.shape

    # Detect balls
    circles = detect_balls(image)

    # Draw detected circles
    draw_circles(circles, image)

    # Save the result to a file instead of displaying it
    output_image_path = 'images/output_detected_circles.jpg'
    cv2.imwrite(output_image_path, image)
    print(f"Output image saved to {output_image_path}")

    # Check coordinates against the corners
    corner_result = check_corners(circles, image_size, threshold=corner_threshold)

    return [(x, y, radius) for x, y, radius in circles], corner_result

def robot_action_based_on_corners(corner_results, client_pc):
    if corner_results["top_left"]:
        print("Ball is near the top-left corner. Robot action: move to top-left.")
        client_pc.send_command("move_to_top_left")
    elif corner_results["top_right"]:
        print("Ball is near the top-right corner. Robot action: move to top-right.")
        client_pc.send_command("move_to_top_right")
    elif corner_results["bottom_left"]:
        print("Ball is near the bottom-left corner. Robot action: move to bottom-left.")
        client_pc.send_command("move_to_bottom_left")
    elif corner_results["bottom_right"]:
        print("Ball is near the bottom-right corner. Robot action: move to bottom-right.")
        client_pc.send_command("move_to_bottom_right")
    else:
        print("No ball near any corner. Robot action: default action.")
        client_pc.send_command("default_action")

# def determine_corner(client_pc, camera, ball_pos):
#     # Take initial image
#     capture_image(camera, "test.jpg")
#     image = cv2.imread("images/capturedImage/test.jpg")
#     # Find corners
#     #corner_point = find_corner_points_full(image)
#     #ball_pos = detect_balls(image)
#     #circles = draw_circles(ball_pos,image)
#     ball_coordinates = get_ball_coordinates(camera)
#     print("Detected ball coordinates:", ball_coordinates)
#     if PIVOT_POINTS[0]:
#         if ball_coordinates

