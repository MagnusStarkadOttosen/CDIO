import cv2

from src.client.field.coordinate_system import find_corner_points_full, warp_perspective
from src.client.field.collect_from_corner import collect_from_corner
from src.client.field.navigate_to_target import navigate_to_target
from src.client.pc_client import ClientPC
from src.client.vision.camera import initialize_camera, capture_image
from src.client.vision.shape_detection import detect_robot

client_pc = ClientPC()


dst_size = (1200, 1800)
tolerance = 10

target_point = (300, 600)

isRobot_moving = False

camera = initialize_camera(index=2)

#take image
capture_image(camera, "test.jpg")
image = cv2.imread("images/capturedImage/test.jpg")

final_points = (10, 600)

def deliver_balls_to_goal(final_point, camera, client_pc , target_point, dst_size=(1200, 1800), tolerance=1)

    capture_image(camera, "test1.jpg")
    image = cv2.imread("images/capturedImage/test1.jpg")

    # Warp image
    gen_warped_image = warp_perspective(image, final_points, dst_size)
    robot_pos, robot_direction = detect_robot(gen_warped_image)

    #navigate_robot_to_target(final_point,camera, client_pc, target_point)
    # If the robot is not in the delivery point
    if robot_pos != target_point:
        navigate_to_target()
    # Navigate the robot to the delivery point
    collect_from_corner(client_pc, target_point, camera)