# from src.vision.shape_detection import Shapes,Pos
import numpy as np

from src.client.utilities import convert_px_to_cm, convert_px_cm_temp, get_distance
from src.client.vision.shape_detection import Shapes


class Route:
    def __init__(self, x, y, d, newAngle, drivingMode):
        self.x = x
        self.y = y
        self.d = d
        self.newAngle = newAngle
        self.drivingMode = drivingMode


def balls_are_remaining(circles):
    if circles is not None:
        return True
    else:
        return False


def find_nearest_ball(robot_pos, circles):
    # ball_pos = (220, 388)  # hard-coded placeholder
    ball_pos = np.array([0, 0])
    nearest = 300000
    for (x, y, r) in circles:
        # width_cm, height_cm = convert_px_cm(circle.x, circle.y)
        # ball = np.array([width_cm, height_cm])
        # print(f"width : {width_cm} heigth: {height_cm}")
        dist = get_distance(robot_pos, np.array([x, y]))
        # print("dist before if: ", dist)
        if dist < nearest:
            ball_pos[0] = x
            ball_pos[1] = y
            # print("dist: ", dist)
            nearest = dist
            print(f"current nearest dist: {nearest}")
    return ball_pos


def findNearestBall(robotpostition, shape: Shapes):
    ball_route = Route(0, 0, 0, 0, " ")
    circles = np.round(shape.circles[0, :]).astype("int")
    if balls_are_remaining:
        nearest = 300000
        for (x, y, r) in circles:
            # width_cm, height_cm = convert_px_cm(circle.x, circle.y)
            # ball = np.array([width_cm, height_cm])
            # print(f"width : {width_cm} heigth: {height_cm}")
            dist = get_distance(robotpostition, np.array([x, y]))
            print("dist before if: ", dist)
            if (dist < nearest):
                ball_route.x = x
                ball_route.y = y
                ball_route.d = convert_px_to_cm(dist)
                print("dist: ", dist)
                nearest = dist

        return ball_route
    else:
        return 0


def findNearestWall(robotpostition, shape: Shapes, route: Route):
    nearest = 300
    lines = np.round(shape.lines[0, :]).astype("int")

    for (x, y, z) in lines:
        width_cm, height_cm = convert_px_cm_temp(x, y)
        ball = np.array([width_cm, height_cm])
        dist = get_distance(robotpostition, ball)
        if (dist < nearest):
            route.x = x
            route.y = y
            route.d = dist


def roboDrive(route: Route, robot_pos, shape: Shapes):
    findNearestBall(robot_pos, shape, route)
    route.drivingmode = "roboDrive"
    return route


def straightDrive(robotPostion, shape: Shapes):
    route = findNearestBall(robotPostion, shape)

    if route:
        target_pos = np.array([route.x, route.y])
        route.drivingmode = "straightDrive"
        # route.newAngle = get_degrees_to_rotation(robotPostion, (route.x, route.y))
    return route, target_pos


def sendRoute(route: Route, pos, shape: Shapes, ):
    # wallPositon= Route(0,0,0,0,"")
    #  findNearestWall(wallPositon)
    # if(wallPositon.d>=minWallDistance):
    #     roboDrive(route,pos,shape)

    # else:
    straightDrive(route, pos, shape)
    return route
