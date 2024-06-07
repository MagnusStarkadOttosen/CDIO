import cv2
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
# from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image, initialize_camera
from src.client.vision.shape_detection import detect_robot


FINAL_POINTS = (0,0)
PIVOT_POINTS = [(300, 600), (1500, 600)]

def navigate_to_target(camera, client_pc, target_point, dst_size=(1200, 1800), tolerance=1):
    is_robot_moving = False

    while True:
        # Take image
        capture_image(camera, "test1.jpg")
        image = cv2.imread("images/capturedImage/test1.jpg")

        corner_point = find_corner_points_full(image)
        # Warp image
        gen_warped_image = warp_perspective(image, corner_point, dst_size)

        # Find robot
        robot_pos, robot_direction = detect_robot(gen_warped_image)

        # If robot at target, stop robot and break
        if are_points_close(robot_pos, target_point, tolerance=100):
            client_pc.send_command("stop")
            is_robot_moving = False
            break

        # Calculate degrees to turn
        angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
        tolerance = 10
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

def navigat_to_pivot(camera, client_pc, pivot_point):
    navigate_to_target(camera, client_pc, pivot_point)
