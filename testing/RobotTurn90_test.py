#steps
#1 take image
#2 find corners
#3 take image
#4 warp image
#5 find robot
#6 if robot at target stop robot and break to 11
#7 calculate degrees to turn
#8 if degrees to turn is not 0 turn robot
#9 if robot not moving start robot
#10 go to 3
#11 print "robot at target point"

import cv2
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.vision.camera import capture_image, close_camera, initialize_camera
from src.client.vision.shape_detection import detect_robot

client_pc = ClientPC()


dst_size = (1200, 1800)
tolerance = 10

target_point = (900, 600)

isRobot_moving = False
print("before cam")
camera = initialize_camera(index=2)
print("after cam")
#take image
print("before image")
capture_image(camera, "test.jpg")
print("after image")
image = cv2.imread("images/capturedImage/test.jpg")
print("after read image")
#find corners
final_points = find_corner_points_full(image, doVerbose=True)

try:
    print("before 1")
    #take image
    capture_image(camera, "test1.jpg")
    image = cv2.imread("images/capturedImage/test1.jpg")
    print("after 1")
    #warp image
    gen_warped_image = warp_perspective(image, final_points, dst_size)
    print("after warp")
    #find robot
    robot_pos, robot_direction = detect_robot(gen_warped_image)
    print(f"robot pos {robot_pos} and direction {robot_direction} before")
    #calculate degrees to turn
    angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
    print(f"angle before {angle}")
    client_pc.send_command(f"turn {angle}")
    robot_pos, robot_direction = detect_robot(gen_warped_image)
    print(f"robot pos {robot_pos} and direction {robot_direction} after")

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    # Cleanup resources
    close_camera(camera) 
    print("after while")
    client_pc.send_command("stop")
    client_pc.send_command("exit")
    client_pc.close_connection()

    print("Robot done moving")