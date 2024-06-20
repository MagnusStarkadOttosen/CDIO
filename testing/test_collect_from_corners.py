import numpy as np
from src.client.field import navigate_to_target
from src.client.field.collect_from_corner import robot_movement_based_on_corners, check_corners, is_ball_in_corner, \
    calculate_distance
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.mainloop import MainLoop
from src.client.field.coordinate_system import warp_perspective
# from src.client.search_targetpoint.a_star_search import find_path
from src.client.vision.shape_detection import detect_balls, detect_robot


print("Test collecting from corners.")

# CAMERA_HEIGHT = 202
# ROBOT_HEIGHT = 23
# scale_factor = (CAMERA_HEIGHT - ROBOT_HEIGHT) / CAMERA_HEIGHT

IMAGE_SIZE = [1200, 1800]
ball_coords_1 = (1690, 574)
ball_coords_2 = (1800, 1200) # bottom_right
#ball_coords_2 = (0, 0) # top_left
# ball_coords_2 = (1800, 0) # top_right
#ball_coords_2 = (0, 1200) # bottom_right

WHITE_BALL_COUNT = 10
ROBOT_CAPACITY = 6
# TOLERANCE = 2
TURN_SPEED = 3
DST_SIZE = (1200, 1800)
PIVOT_POINTS = [(300, 600), (1500, 600)]
CORNERS = {
    "top_left": (0, 0),
    "bottom_left": (0, 1200),
    "top_right": (1800, 0),
    "bottom_right": (1800, 1200)
}

# Original target positions
targets = [
    (0, 0),          # Scenario 1: Top Left
    (0, 1200),       # Scenario 2: Bottom Left
    (1800, 0),       # Scenario 3: Top Right
    (1800, 1200)     # Scenario 4: Bottom Right
]
# Define the function to adjust position
# def adjust_target_position(original_position, scale_factor):
#     adjusted_x = original_position[0] * scale_factor
#     adjusted_y = original_position[1] * scale_factor
#     return (adjusted_x, adjusted_y)

main_loop = MainLoop()
main_loop.initialize_field()
main_loop.client.send_command("start_drive 30")

# Test one corner at the time
if is_ball_in_corner(ball_coords_2):
    print("Checking if the ball is in the corner.")
    print(f"There is a ball in {ball_coords_2} ")
    corner_result_2 = check_corners(ball_coords_2, threshold=50)
    print("corner result 2", corner_result_2)
    pivot_points, corner_points = robot_movement_based_on_corners(corner_result_2)
    print(f"pivot: {pivot_points} corner: {corner_points}")

    # Adjust corner points based on camera perspective
    #corrected_corner_point = adjust_target_position(corner_points, scale_factor)

    print("before navigate to pivot points")
    main_loop._navigate_to_target([pivot_points])
    print("after navigate to pivot points")

    #corrected_distance = calculate_distance(pivot_points, corrected_corner_point)
    distance_to_move = calculate_distance(pivot_points, corner_points)
    print(f"distance to move after scaling: {distance_to_move}")
    main_loop.client.send_command("stop")

    robot_pos, robot_direction = main_loop.temp()
    print(f"Robot Position: {robot_pos}, Robot Direction: {robot_direction}")

    angle = rotate_vector_to_point(robot_pos, robot_direction, ball_coords_2)

    tolerance = 0.5
    if angle < -tolerance or angle > tolerance:
        print(f"The angle is: {angle}")
        main_loop._course_correction(angle, ball_coords_2, tol=tolerance)


    main_loop.client.send_command("start_collect")
    main_loop.client.send_command("move " + str(distance_to_move))
    main_loop.client.send_command("move " + str(-distance_to_move))


    main_loop.client.send_command("stop")
    main_loop.client.send_command("stop_collect")
else:
    print("Ball is not in any corners.")
print("Delivery process started successfully.")



# Loop through each corner scenario
# for corner_name, target in CORNERS.items():
#     if is_ball_in_corner(target):  # Assuming this function can check for specific target
#         print(f"Checking if the ball is in the {corner_name} corner.")
#         corner_result = check_corners(target, threshold=50)
#         print(f"Corner result for {corner_name}: {corner_result}")
#         pivot_points = PIVOT_POINTS[0] if corner_name in ["top_left", "bottom_left"] else PIVOT_POINTS[1]
#         corrected_target = adjust_target_position(target, scale_factor)
#
#         print(f"Before navigate to pivot points for {corner_name}")
#         main_loop._navigate_to_target([pivot_points])
#         print(f"After navigate to pivot points for {corner_name}")
#
#         distance = calculate_distance(pivot_points, corrected_target)
#         distance_to_move = distance * scale_factor
#         print(f"Distance to move after scaling for {corner_name}: {distance_to_move}")
#
#         robot_pos, robot_direction = main_loop.temp()
#         print(f"Robot Position: {robot_pos}, Robot Direction: {robot_direction}")
#
#         angle = rotate_vector_to_point(robot_pos, robot_direction, target)
#
#         tolerance = 0.5
#         if abs(angle) > tolerance:
#             print(f"Angle correction needed for {corner_name}: {angle}")
#             main_loop._course_correction(angle, target, tolerance)
#
#         main_loop.client.send_command("start_collect")
#         main_loop.client.send_command(f"move {distance_to_move}")
#         main_loop.client.send_command("move -50")
#         main_loop.client.send_command("stop")
#         main_loop.client.send_command("stop_collect")
#
#     else:
#         print(f"No ball detected in the {corner_name} corner.")
#
# print("Delivery process completed.")





