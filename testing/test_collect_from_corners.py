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

IMAGE_SIZE = [1200, 1800]
ball_coords_1 = (1690, 574)
# ball_coords_2 = (1800, 1200) # bottom_right
#ball_coords_2 = (0, 0) # top_left
ball_coords_2 = (1800, 0) # top_right
#ball_coords_2 = (0, 1200) # bottom_right

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

main_loop = MainLoop()
main_loop.initialize_field()
main_loop.client.send_command("start_drive 30")

if is_ball_in_corner(ball_coords_2):
    print("Checking if the ball is in the corner.")
    print(f"There is a ball in {ball_coords_2} ")
    corner_result_2 = check_corners(ball_coords_2, threshold=50)
    print("corner result 2", corner_result_2)
    pivot_points, corner_points = robot_movement_based_on_corners(corner_result_2)
    print(f"pivot: {pivot_points} corner: {corner_points}")

    print("before navigate to pivot points")
    main_loop._navigate_to_target([pivot_points])
    print("after navigate to pivot points")

    main_loop.client.send_command("stop")

    robot_pos, robot_direction = main_loop.temp()
    print(f"Robot Position: {robot_pos}, Robot Direction: {robot_direction}")

    angle = rotate_vector_to_point(robot_pos, robot_direction, ball_coords_2)

    tolerance = 1
    if angle < -tolerance or angle > tolerance:
        print(f"The angle is: {angle}")
        main_loop._course_correction(angle, ball_coords_2, tol=tolerance)

    main_loop.client.send_command("start_collect")
    main_loop.client.send_command("move 49")
    main_loop.client.send_command("move -50")
    main_loop.client.send_command("stop")
    main_loop.client.send_command("stop_collect")
else:
    print("Ball is not in any corners.")
print("Delivery process started successfully.")









