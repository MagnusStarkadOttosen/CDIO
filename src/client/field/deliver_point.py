
import math
from src.client.field.navigate_robot_to_target import *
# from src.client.pc_client import ClientPC


target_point = (300, 600)
#turn_angle = 75
corner_point = (0, 0)
# client_pc = ClientPC()


def calculate_distance(corner_point, target_point):
    return math.sqrt((target_point[0] - corner_point[0]) ** 2 + (target_point[1] - corner_point[1]) ** 2)


def deliver_points(client_pc, target_point, camera):
    # Take initial image
    capture_image(camera, "test.jpg")
    image = cv2.imread("images/capturedImage/test.jpg")
    # Find corners
    final_points = find_corner_points_full(image)

    dist=calculate_distance(corner_point, target_point)
    print("test1")
    navigate_robot_to_target(final_points, camera, client_pc, target_point)
    print("test2")
    capture_image(camera, "test1.jpg")
    image = cv2.imread("images/capturedImage/test1.jpg")
    dst_size = (1200, 1800)
    gen_warped_image = warp_perspective(image, final_points, dst_size)
    robot_pos, robot_direction = detect_robot(gen_warped_image)
    turn_angle =  rotate_vector_to_point(target_point, robot_direction, target_point)
    client_pc.send_command(f"turn {turn_angle}")
    print("I am in deliver point")
    client_pc.send_command("start_collect")
    navigate_robot_to_target(client_pc,corner_point)

    client_pc.send_command("start_drive")
    client_pc.send_command(f"drive_backwards {dist}")
    client_pc.send_command(f"turn {-turn_angle}")
    client_pc.send_command("stop")
