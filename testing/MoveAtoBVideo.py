from time import sleep
import cv2
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.vision.shape_detection import detect_robot


client_pc = ClientPC()

turnSpeed = 5

dst_size = (1200, 1800)
tolerance = 10

target_point = (1200, 600)

isRobot_moving = False
isRobot_turning = False

# Capture from camera
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
dst_size = (1200, 1800)
ret, frame = cap.read()
final_points = find_corner_points_full(frame, doVerbose=False)
try:
    while(True):
        #take frame
        ret, frame = cap.read()

        #warp image
        gen_warped_image = warp_perspective(frame, final_points, dst_size)

        #find robot
        robot_pos, robot_direction = detect_robot(gen_warped_image)
        if robot_pos is None or robot_direction is None:
            continue
        print(f"after robot pos {robot_pos} and direction {robot_direction}")
        
        #if robot at target stop robot and break
        if are_points_close(robot_pos, target_point):
            client_pc.send_command("stop")
            isRobot_moving = False
            break

        #calculate degrees to turn
        angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
        # print("after angle")
        #Check if angle need to change
        while angle < -tolerance or angle > tolerance:
            ret, frame = cap.read()
            gen_warped_image = warp_perspective(frame, final_points, dst_size)
            robot_pos, robot_direction = detect_robot(gen_warped_image)
            print(f"after robot pos {robot_pos} and direction {robot_direction}")
            if robot_pos is None or robot_direction is None:
                continue
            angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
            print(f"angle: {angle}")
            if not isRobot_turning:
                isRobot_turning = True
                client_pc.send_command(f"turn_left {turnSpeed}")
            else:
                isRobot_turning = False
        if isRobot_turning:
            isRobot_turning = False
            client_pc.send_command("stop")

        # print("after if 2")
        if not isRobot_moving and not isRobot_turning:
            client_pc.send_command("start_drive")
            isRobot_moving = True
        # print("after if 3")
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    # Cleanup resources
    cap.release()
    print("after while")
    client_pc.send_command("stop")
    client_pc.send_command("exit")
    client_pc.close_connection()

    print("Robot done moving")