import time
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.client.hsvLoad import read_hsv_values
from src.client.field.coordinate_system import warp_perspective
from src.client.search_targetpoint.obstacle_search import is_ball_in_obstacle, obstacle_Search
from src.client.search_targetpoint.buffer_zone_search import buffer_zone_search, is_ball_in_buffer_zone
from src.client.pathfinding.GenerateNavMesh import  GenerateNavMesh, astar
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.vision.shape_detection import detect_balls, detect_obstacles, detect_robot
from src.client.vision.filters import filter_image
from src.mainloop import MainLoop

DST_SIZE = (1200, 1800)


def test_collect_ball_in_obstacle(ml,camera, final_point, direction_color, pivot_color, client):
    ret, frame = ml.camera.read()
    if not ret or frame is None or frame.size == 0:
        print("Failed to read from camera or empty frame captured.")
        return

    warped_img = warp_perspective(frame, ml.final_points, DST_SIZE)
    if warped_img is None or warped_img.size == 0:
        print("Failed to warp image or warped image is empty.")
        return

    print(f"testing colors {ml.direction_color}")
    robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)
    while robot_pos is None or robot_direction is None:
        robot_pos, robot_direction = detect_robot(warped_img, ml.direction_color, ml.pivot_color)

    white_hsv_values = read_hsv_values('hsv_presets_white.txt')
    red_hsv_values = read_hsv_values('hsv_presets_red.txt')
    navmesh = GenerateNavMesh(warped_img, red_hsv_values)

    try:
        filtered_img = filter_image(warped_img, hsv_values=white_hsv_values)
        if filtered_img is None or filtered_img.size == 0:
             print("Filtered image is empty.")
             return
    except Exception as e:
         print(f"Error in filtering image: {e}")
         return

    balls = detect_balls(filtered_img)
    print(f"balls {balls}")
    if len(balls)<1:
        print("No balls detected.")
        return

    midpoint = detect_obstacles(filtered_img)
    print(f"midpoint {midpoint}")
# check if ball in balls is in obstacle
    for ball in balls:
        if is_ball_in_obstacle(ball, midpoint):
            target_point, target = obstacle_Search(ball, midpoint)
            path = astar(navmesh, robot_pos, target)
            # path = [target]
            print(f"path: {path} target point: {target_point} target: {target}")
            ml._navigate_to_target(path)
            angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
            print(f"after robot pos {robot_pos} and direction {robot_direction} and target {target_point} and angle: {angle}")
            if angle < -0.5 or angle > 0.5:
                ml._course_correction(angle, ball, tol=0.5)
            ml.client.send_command("start_collect")
            ml.client.send_command("move 7")
            time.sleep(0.5)
            ml.client.send_command("move 1")
            time.sleep(0.5)
            ml.client.send_command("move 0.5")
            time.sleep(0.5)
            ml.client.send_command("move 0.5")
            time.sleep(0.5)
            ml.client.send_command("move 0.5")
            time.sleep(0.5)
            ml.client.send_command("move 0.5")
            time.sleep(0.5)
            ml.client.send_command("move 0.5")
            time.sleep(0.5)
            ml.client.send_command("move 0.5")
            time.sleep(0.5)
            ml.client.send_command("move -10")
            ml.client.send_command("stop_collect")
            ml.client.send_command("stop")
            return
        elif is_ball_in_buffer_zone(ball):
            target_point = buffer_zone_search(ball)
            path = astar(ml.o4navmesh, robot_pos, target_point)
            ml._navigate_to_target(path)
            angle = rotate_vector_to_point(robot_pos, robot_direction, ball)
            print(f"after robot pos {robot_pos} and direction {robot_direction} and target {ball} and angle: {angle}")
            if angle < -0.5 or angle > 0.5:
                ml._course_correction(angle, ball, tol=0.5)
            ml.client.send_command("start_collect")
            ml.client.send_command("move 5")
            time.sleep(0.5)
            ml.client.send_command("move 1")
            time.sleep(0.5)
            ml.client.send_command("move -6")
            ml.client.send_command("stop_collect")
            ml.client.send_command("stop")
            return
    print("No balls in buffer zone or obstacle.")


main_loop = MainLoop()
main_loop.initialize_field()
main_loop._detect_initial_balls()
main_loop._detect_obstacles()
test_collect_ball_in_obstacle(main_loop, main_loop.camera, main_loop.final_points, main_loop.direction_color, main_loop.pivot_color, main_loop.client)



# if __name__ == "__main__":
#     ml = MainLoop()
#     ml.initialize_field()
#     ml._detect_initial_balls()
#     test_collect_ball_in_obstacle(ml, ml.camera, ml.final_points, ml.direction_color, ml.pivot_color, ml.client)
#     ml.client.send_command("stop")
#     ml.client.send_command("stop_collect")
#     ml.camera.release()
#     cv2.destroyAllWindows()
#     sys.exit(0)

