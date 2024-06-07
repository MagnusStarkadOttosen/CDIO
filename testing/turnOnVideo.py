
import cv2
from src.client.field.coordinate_system import find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.vision.shape_detection import detect_robot

turnTo = "Left"

turnSpeed = 20

client_pc = ClientPC()

dst_size = (1200, 1800)
tolerance = 10

left_point = (0, 600)
right_point = (1800, 600)

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
        
        #calculate degrees to turn
        if turnTo == "Left":
            angle = rotate_vector_to_point(robot_pos, robot_direction, left_point)
        else:
            angle = rotate_vector_to_point(robot_pos, robot_direction, right_point)

        while angle < -tolerance or angle > tolerance:
            gen_warped_image = warp_perspective(frame, final_points, dst_size)
            robot_pos, robot_direction = detect_robot(gen_warped_image)
            if robot_pos is None or robot_direction is None:
                continue
            client_pc.send_command(f"turn_left {turnSpeed}")
        client_pc.send_command("stop")

        if turnTo == "Left":
            turnTo = "Right"
        else:
            turnTo = "Left"
        
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