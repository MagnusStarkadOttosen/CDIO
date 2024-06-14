import numpy as np
from src.client.field import navigate_to_target
from src.client.field.collect_from_corner import robot_movement_based_on_corners, check_corners, is_ball_in_corner
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.mainloop import MainLoop
from src.client.field.coordinate_system import warp_perspective
# from src.client.search_targetpoint.a_star_search import find_path
from src.client.vision.shape_detection import detect_balls, detect_robot


print("Test collecting from corners.")
# client_pc = ClientPC()


IMAGE_SIZE = [1200, 1800]
ball_coords_1 = (1690, 574)
ball_coords_2 = (1790, 10)

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
TOLERANCE = 2
TURN_SPEED = 3
DST_SIZE = (1200, 1800)
PIVOT_POINTS = [(300, 600), (1500, 600)]
CORNERS = {
    "top_left": (0, 0),
    "bottom_left": (0, 1200),
    "top_right": (1800, 0),
    "bottom_right": (1800, 1200)
}

# try:
    # corner_results = check_corners(ball_coords)
    # robot_movement_based_on_corners(corner_results)
main_loop = MainLoop()
main_loop.initialize_field()
# if is_ball_in_corner(ball_coords_1):
#     corner_result = check_corners(ball_coords_1, threshold=50)
#     pivot_points, corner_points = robot_movement_based_on_corners(corner_result)
#     main_loop._navigate_to_target(pivot_points)
#     main_loop.client.send_command("stop")
#     main_loop._navigate_to_target(corner_points)
# else:
#     print("Ball is not in any corners.")
if is_ball_in_corner(ball_coords_2):
    print(f"There is a ball in {ball_coords_2} ")
    corner_result_2 = check_corners(ball_coords_2, threshold=50)
    print("saddfsd19243284")
    pivot_points, corner_points = robot_movement_based_on_corners(corner_result_2)
    print(f"pivot: {pivot_points} corner: {corner_points}")

    temp = [pivot_points]
    print(f"temp: {temp}")
    # main_loop.client.send_command("start_collect")
    main_loop._navigate_to_target(temp)
    main_loop.client.send_command("stop")
    main_loop.client.send_command("start_collect")
    main_loop._navigate_to_target(temp) # we are here


    # robot_pos, robot_direction = main_loop.temp()
    # angle = rotate_vector_to_point(robot_pos, robot_direction, ball_coords_2)
    # print(f"after robot pos {robot_pos} and direction {robot_direction} and target {ball_coords_2} and angle: {angle}")
    # if angle < -TOLERANCE or angle > TOLERANCE:
    #     print(f"asdsdkjfsdkjfsdkj {angle}")
    #     main_loop._course_correction(angle, ball_coords_2)
    #
    # main_loop.client.send_command("move 60")
    #
    # main_loop.client.send_command("move -50")
    #
    # main_loop.client.send_command("stop")


    # main_loop._navigate_to_target(pivot_points)
    # main_loop._navigate_to_target(corner_points)

else:
    print("Ball is not in any corners.")
print("Delivery process started successfully.")
# except Exception as e:
#     print(f"An error occurred during the delivery process: {str(e)}")











