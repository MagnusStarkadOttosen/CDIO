
import math

import numpy as np

from src.client.field.navigate_to_target import *
from src.client.pc_client import ClientPC
from src.client.vision.shape_detection import detect_balls
from testing.visualization import draw_circles

# from src.client.pc_client import ClientPC


#target_point = (300, 600)
#turn_angle = 75
CORNERS = [(0, 0), (0, 1200), (1800, 0), (1800, 1200)]
PIVOT_POINTS = [(300, 600), (1500, 600)]
IMAGE_SIZE = [1200,1800]
# client_pc = ClientPC()

def initialize():
    global client_pc, camera
    client_pc = ClientPC()
    camera = initialize_camera(index=2)

def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)


def collect_from_corner(client_pc, camera, corner_point):
    # Take initial image
    capture_image(camera, "test.jpg")
    image = cv2.imread("images/capturedImage/test.jpg")
    # Find corners
    #corner_point = find_corner_points_full(image)


    #dist=calculate_distance(corner_point, target_point)
    print("Read image")
    client_pc.send_command("start_collect")

    # Check corners
   # ball_coordinates, corner_result = get_ball_coordinates(camera)
    #print("Detected ball coordinates:", ball_coordinates)
    #robot_action_based_on_corners(corner_result,client_pc,PIVOT_POINTS)

    #navigat_to_pivot(camera, client_pc,)
    navigate_to_target(camera, client_pc, corner_point)
    print("After navigating to the target")
    capture_image(camera, "test1.jpg")
    image = cv2.imread("images/capturedImage/test1.jpg")
    dst_size = (1200, 1800)
    gen_warped_image = warp_perspective(image, CORNERS, dst_size)
    robot_pos, robot_direction = detect_robot(gen_warped_image)
    print("After detect robot")
    # turn_angle =  rotate_vector_to_point(robot_pos, robot_direction, corner_point)
    # client_pc.send_command(f"turn {turn_angle}")
    # print("I am in deliver point")

    #navigate_robot_to_target(target_point, camera, client_pc,corner_point)

    # client_pc.send_command("start_drive")
    # client_pc.send_command(f"drive_backwards {dist}")
    # client_pc.send_command(f"turn {-turn_angle}")
    client_pc.send_command("stop")


def check_corners(circles, IMAGE_SIZE, threshold=50):
    corners = {
        "top_left": (0, 0),
        "top_right": (IMAGE_SIZE[1], 0),
        "bottom_left": (0, IMAGE_SIZE[0]),
        "bottom_right": (IMAGE_SIZE[1], IMAGE_SIZE[0])
    }
    corner_results = {
        "top_left": False,
        "top_right": False,
        "bottom_left": False,
        "bottom_right": False
    }

    for x, y, radius in circles:
        if np.linalg.norm(np.array([x, y]) - np.array(corners["top_left"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the top-left corner.")
            corner_results["top_left"] = True
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["top_right"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the top-right corner.")
            corner_results["top_right"] = True
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_left"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the bottom-left corner.")
            corner_results["bottom_left"] = True
        elif np.linalg.norm(np.array([x, y]) - np.array(corners["bottom_right"])) < threshold:
            print(f"Ball at ({x}, {y}) is near the bottom-right corner.")
            corner_results["bottom_right"] = True

    return corner_results

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

def robot_action_based_on_corners(corner_results, client_pc, PIVOT_POINTS):
    if corner_results["top_left"]:
        print("Ball is near the top-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to top-left.")
        #client_pc.send_command(f"move_to {PIVOT_POINTS[0]} ")
        navigat_to_pivot(camera, client_pc, PIVOT_POINTS[0])
        collect_from_corner(client_pc, camera, CORNERS[0])  # navigate to top-left
    elif corner_results["bottom_left"]:
        print("Ball is near the bottom-left corner. Robot action: move to PIVOT_POINT 0 and then navigate to bottom-left.")
        #client_pc.send_command(f"move_to {PIVOT_POINTS[0]}")
        navigat_to_pivot(camera, client_pc, PIVOT_POINTS[0])
        navigate_to_target(CORNERS, camera, client_pc, CORNERS[1])  # navigate to bottom-left
    elif corner_results["top_right"]:
        print("Ball is near the top-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to top-right.")
        #client_pc.send_command(f"move_to {PIVOT_POINTS[1]} ")
        navigat_to_pivot(camera, client_pc, PIVOT_POINTS[1])
        navigate_to_target(CORNERS, camera, client_pc, CORNERS[2])  # navigate to top-right
    elif corner_results["bottom_right"]:
        print("Ball is near the bottom-right corner. Robot action: move to PIVOT_POINT 1 and then navigate to bottom-right.")
        #client_pc.send_command(f"move_to {PIVOT_POINTS[1]}")
        navigat_to_pivot(camera, client_pc, PIVOT_POINTS[1])
        navigate_to_target(CORNERS, camera, client_pc, CORNERS[3])  # navigate to bottom-right
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

