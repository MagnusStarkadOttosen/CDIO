
from client.field.coordinate_system import warp_perspective
from client.pathfinding.CalculateCommandList import rotate_vector_to_point
from client.search_targetpoint.obstacle_search import obstacle_Search
from client.vision.filters import filter_image
from client.vision.shape_detection import detect_balls, detect_obstacles, detect_robot
from mainloop import MainLoop


DST_SIZE = (1200, 1800)
# make a test for collect ball in obstacle area : robot have to move to the targetpoint,
# # have to turn in the right direction to the target point before executing commands
def test_collect_ball_in_obstacle(ml):
    ret, frame = ml.camera.read()
    warped_img = warp_perspective(frame, ml.final_points, DST_SIZE)
    print(f"testing colors {ml.direction_color}")
    robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)
    while robot_pos is None or robot_direction is None:
        robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)
    
    ball = detect_balls(filter_image(warped_img, "filter_image_white"))

    midpoint = detect_obstacles(filter_image(warped_img, "filter_image_red"))
    target_point, target = obstacle_Search(ball[0], 0, 1, midpoint)
    path = [target_point]
    ml._navigate_to_target(path)
    
    angle = rotate_vector_to_point(robot_pos, robot_direction,target)
    print(f"after robot pos {robot_pos} and direction {robot_direction} and target {target} and angle: {angle}")
    if angle < -1 or angle > 1:
        ml._course_correction(angle, target,tol=1)
    ml.client.send_command("move 7")
    ml.client.send_command("move -7")
    ml.client.send_command("stop_collect")
    ml.client.send_command("stop")




main_loop = MainLoop()
main_loop.initialize_field()
test_collect_ball_in_obstacle(main_loop)
