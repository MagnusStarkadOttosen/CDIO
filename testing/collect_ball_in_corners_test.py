import time

from client.search_targetpoint.buffer_zone_search import buffer_zone_search
from src.client.field.coordinate_system import warp_perspective
from src.client.hsvLoad import read_hsv_values
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.search_targetpoint.obstacle_search import obstacle_Search
from src.client.vision.filters import filter_image
from src.client.vision.shape_detection import detect_balls, detect_obstacles, detect_robot
from src.mainloop import MainLoop


DST_SIZE = (1200, 1800)
# make a test for collect ball in obstacle area : robot have to move to the targetpoint,
# # have to turn in the right direction to the target point before executing commands
def test_collect_ball_in_corners(ml):
    ret, frame = ml.camera.read()
    warped_img = warp_perspective(frame, ml.final_points, DST_SIZE)
    print(f"testing colors {ml.direction_color}")
    robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)
    while robot_pos is None or robot_direction is None:
        robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)

    white_hsv_values = read_hsv_values('hsv_presets_white.txt')
    red_hsv_values = read_hsv_values('hsv_presets_red.txt')

    ball = detect_balls(filter_image(warped_img, hsv_values=white_hsv_values,))
    print(f"ball {ball}")
    target_point= buffer_zone_search(ball[0], 0, 1)
    path = [target_point]
    ml._navigate_to_target(path)
    
    angle = rotate_vector_to_point(robot_pos, robot_direction,ball[0])
    print(f"after robot pos {robot_pos} and direction {robot_direction} and target {ball} and angle: {angle}")
    if angle < -0.5 or angle > 0.5:
        ml._course_correction(angle, ball,tol=0.5)
    # ml.client.send_command("start_collect")
    # ml.client.send_command("move 5")
    # time.sleep(0.5)
    # ml.client.send_command("move 1")
    # time.sleep(0.5)
    # ml.client.send_command("move -6")
    # ml.client.send_command("stop_collect")
    # ml.client.send_command("stop")




main_loop = MainLoop()
main_loop.initialize_field()
test_collect_ball_in_corners(main_loop)
