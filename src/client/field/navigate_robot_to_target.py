import cv2
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image
from src.client.vision.shape_detection import detect_robot


def navigate_robot_to_target(client_pc, target_point, dst_size=(1200, 1800), tolerance=1):
    is_robot_moving = False

    # Take initial image
    capture_image("test.jpg")
    image = cv2.imread("images/capturedImage/test.jpg")
    # Find corners
    final_points = find_corner_points_full(image)

    while True:
        # Take image
        capture_image("test1.jpg")
        image = cv2.imread("images/capturedImage/test1.jpg")

        # Warp image
        gen_warped_image = warp_perspective(image, final_points, dst_size)

        # Find robot
        robot_pos, robot_direction = detect_robot(gen_warped_image)

        # If robot at target, stop robot and break
        if are_points_close(robot_pos, target_point, tolerance):
            client_pc.send_command("stop")
            is_robot_moving = False
            break

        # Calculate degrees to turn
        angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)

        # Check if angle needs to change
        if angle < -tolerance or angle > tolerance:
            if is_robot_moving:
                client_pc.send_command("stop")
                is_robot_moving = False
            client_pc.send_command(f"turn {angle}")

        if not is_robot_moving:
            client_pc.send_command("start_drive")
            is_robot_moving = True
    print("Robot done moving")
