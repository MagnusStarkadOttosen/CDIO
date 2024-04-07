import math
from src.client.vision.shape_detection import detect_balls
from src.client.vision.filters import filter_image_red, filter_image_green
from src.client.utilities import get_distance

WHEEL_DIMENSION = 5.5
DIST_BETWEEN_WHEELS = 13.5
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


# modified robot class with position and pivot
# the robot's position in the coordinate system with two points ( red and green) is called A and B
# A and B is get from the image detection with the red and green points from decetor_robot.py
# M is the intersection point between the line AB and the wheel axis with distan M to A is 10 cm
# M is the robot's position

# the robot's position is updated after the robot moves or turns
# the pivot is updated after the robot turns
# the robot's position is updated after the robot moves

class Robot:
    def __init__(self):
        self.red_dot = None  # red point's coordinates
        self.green_dot = None  # green point's coordinates
        self.pos = None  # the robot's position
        self.pivot = 0  # the angle between the vector pos->green and vector pos->ball_pos

    def update_robot_pos(self, green_pos, red_pos):
        # red = detect_ball(filter_image_red(image))
        # green = detect_ball(filter_image_green(image))
        # if filter_image_red(image) is not None:
        #     if red is not None:
        #         self.red_dot = (red[0], red[1])  # Extract x and y coordinates
        #     else:
        #         self.red_dot = None
        #
        # distance from A to B, TODO make dist A->B a constant value and delete if statement
        if self.red_dot or self.green_dot is None:
            self.update_dot_positions(green_pos, red_pos)
        distance = math.sqrt(
            (self.green_dot[0] - self.red_dot[0]) ** 2 + (self.green_dot[1] - self.red_dot[1]) ** 2)
        # distance from A to M :a
        a = 10
        self.update_dot_positions(green_pos, red_pos)
        self.pos = (self.red_dot[0] + a / (distance * (self.green_dot[0] - self.red_dot[0])),
                    self.red_dot[1] + a / (distance * (self.green_dot[1] - self.red_dot[1])))

    def update_dot_positions(self, green_pos, red_pos):
        if len(green_pos) > 1 and len(red_pos) > 1:
            self.green_dot = [green_pos[0], green_pos[1]]
            self.red_dot = [red_pos[0], red_pos[1]]
        else:
            print("Green or red position missing coordinate")

    def update_pivot_from_image(self, ball_pos):
        # self.C = target_pos # There is no member C in Robot??
        self.pivot = self.get_degrees_to_rotate(ball_pos)

    def move(self, target_pos):
        # distance to move is the distance from M to the target position
        # the robot's position is updated after the robot moves
        get_distance(self, target_pos)
        self.pos = target_pos
        return self.pos

    def get_degrees_to_rotate(self, target_pos):
        # distance MB = a
        a = math.sqrt((self.green_dot[0] - self.pos[0]) ** 2 + (self.green_dot[1] - self.pos[1]) ** 2)
        # distance MC = b
        b = math.sqrt((target_pos[0] - self.pos[0]) ** 2 + (target_pos[1] - self.pos[1]) ** 2)
        # distance BC = c
        c = math.sqrt((target_pos[0] - self.green_dot[0]) ** 2 + (target_pos[1] - self.green_dot[1]) ** 2)
        # radian of angle between vector MB and vector MC
        radian = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
        # degrees of angle between vector MB and vector MC
        degrees = math.degrees(radian)
        # determine the robot's rotation direction relative to the target position
        # turn left or turn right
        # Calculate direction vectors
        MB = (self.green_dot[0] - self.pos[0], self.green_dot[1] - self.pos[1])
        MTarget = (target_pos[0] - self.pos[0], target_pos[1] - self.pos[1])

        # Calculate the cross product's Z component
        cross_product_z = MB[0] * MTarget[1] - MB[1] * MTarget[0]

        # Determine direction based on the cross product's sign
        if cross_product_z > 0:
            return -degrees
        elif cross_product_z < 0:
            return degrees
        else:
            return 0
