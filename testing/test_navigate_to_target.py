import cv2
from src.client.field.coordinate_system import are_points_close, find_corner_points_full, warp_perspective
from src.client.pathfinding.CalculateCommandList import rotate_vector_to_point
from src.client.pc_client import ClientPC
from src.client.search_targetpoint.a_star_search import find_path
from src.client.vision.filters import filter_image_orange
from src.client.vision.shape_detection import detect_balls, detect_robot
from src.mainloop import MainLoop

ml = MainLoop()
final_points = ml.initialize_field()

# client_pc = ClientPC()
#
turnSpeed = 3
#
dst_size = (1200, 1800)
tolerance = 5
#
target_found = False
ball_collected = False
at_goal = False
#
#
# isRobot_moving = False
# isRobot_turning = False
#
# cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
# dst_size = (1200, 1800)
# ret, frame = cap.read()
# final_points = find_corner_points_full(frame, doVerbose=False)
#
# goal_point = (600, 600)

ml.client.send_command("start_collect")

try:
    while(True):
        while(True):
            # take frame
            ret, frame = ml.camera.read()

            # warp image
            gen_warped_image = warp_perspective(frame, ml.final_points, dst_size)

            if not target_found:
                orange_image = filter_image_orange(gen_warped_image)
                temp = detect_balls(orange_image)
                x, y, r = temp[0]
                target_point = (x, y)
                target_found = True


            # find robot
            robot_pos, robot_direction = detect_robot(gen_warped_image)
            if robot_pos is None or robot_direction is None:
                continue
            print(f"after robot pos {robot_pos} and direction {robot_direction} and target {target_point}")
            # path = find_path(ml.grid, robot_pos, target_point)
            path = [(target_point[0], target_point[1])]
            ml._navigate_to_target(path)

        # after ball collected

        #check if ball collected
        # orange_image = filter_image_orange(gen_warped_image)
        # temp = detect_balls(orange_image)
        # if len(temp) != 0:
        #     continue
        # else:

        #change target point
        if not ball_collected:
            ball_collected = True
            target_point = (200,600)
            continue

        #point to goal
        if ml.at_target:
            target_point = (0,600)
            angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
            while angle < -tolerance or angle > tolerance:
                ret, frame = ml.camera.read()
                gen_warped_image = warp_perspective(frame, ml.final_points, dst_size)
                robot_pos, robot_direction = detect_robot(gen_warped_image)
                print(f"after robot pos {robot_pos} and direction {robot_direction}")
                if robot_pos is None or robot_direction is None:
                    continue
                angle = rotate_vector_to_point(robot_pos, robot_direction, target_point)
                print(f"angle: {angle}")
                if not ml.robot_is_turning and angle < 0:
                    ml.robot_is_turning = True
                    robot_ = False
                    ml.client.send_command(f"turn_left {-turnSpeed}")
                elif not ml.robot_is_turning and angle >= 0:
                    ml.robot_is_turning = True
                    ml.robot_is_moving = False
                    ml.client.send_command(f"turn_left {turnSpeed}")
                else:
                    ml.robot_is_turning = False

        #deliver
        ml.client.send_command("stop")
        ml.client.send_command("deliver")
        break

        
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    # Cleanup resources
    ml.camera.release()
    print("after while")
    ml.client.send_command("stop")
    ml.client.send_command("exit")
    ml.client.close_connection()

    print("Robot done moving")




