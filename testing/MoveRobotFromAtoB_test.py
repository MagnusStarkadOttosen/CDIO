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
from src.client.vision.camera import capture_image
from src.client.vision.shape_detection import detect_robot

client_pc = ClientPC()


dst_size = (1200, 1800)
tolerance = 1

target_point = (900, 600)

isRobot_moving = False

#take image
capture_image("test.jpg")
image = cv2.imread("images/capturedImage/test.jpg")
#find corners
final_points = find_corner_points_full(image)

while(True):
    #take image
    capture_image("test.jpg")
    image = cv2.imread("images/capturedImage/test.jpg")
    
    #warp image
    gen_warped_image = warp_perspective(image, final_points, dst_size)
    
    #find robot
    robot_pos, robot_direction = detect_robot(gen_warped_image)
    
    #if robot at target stop robot and break
    if are_points_close(robot_pos, target_point):
        client_pc.send_command("stop")
        isRobot_moving = False
        break
    
    #calculate degrees to turn
    angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
    
    #Check if angle need to change
    if angle < -tolerance or angle > tolerance:
        if isRobot_moving:
            client_pc.send_command("stop")
            isRobot_moving = False
        client_pc.send_command("turn " + angle)
    
    if not isRobot_moving:
        client_pc.send_command("move")
        isRobot_moving = True
        
    
    
    
#TODO: send exit command to shut down the server

print("Robot done moving")