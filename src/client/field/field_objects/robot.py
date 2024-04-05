import math
from src.client.vision import detect_ball
from src.client.field.coordinate_system import filter_image_red
from src.client.field.coordinate_system import filter_image_green
from src.client.vision.wheel_movement import get_degrees_to_rotation
from src.client.vision.wheel_movement import get_distance_to_move
WHEEL_DIMENSION = 80
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
        self.A = None # red point's coordinates
        self.B = None # green point's coordinates
        self.M = None # the robot's position
        self.pivot = 0 # the angle between the tector MB and tector MC with C is the ball's position
        

    def update_AB_andM_from_image(self, image):
        red_point = detect_ball(filter_image_red(image))
        green_point = detect_ball(filter_image_green(image))
        if filter_image_red(image) is not None:
            if red_point is not None:
                self.A = (red_point[0], red_point[1])  # Extract x and y coordinates
            else:
                self.A = None

        if filter_image_green(image) is not None:
             if green_point is not None:
                 self.B = (green_point[0], green_point[1])
             else:
                 self.B = None

         # distance from A to B
             distance = math.sqrt((self.B[0] - self.A[0]) ** 2 + (self.B[1] - self.A[1]) ** 2)
         # distance from A to M :a
             a = 10
             self.M = (red_point[0]+ a/(distance*(green_point[0]-red_point[0])), red_point[1] + a/(distance*(green_point[1]-red_point[1])))
        return self.A, self.B, self.M

    def update_pivot_from_image(self, target_pos):
        self.C = target_pos
        get_degrees_to_rotation(self, target_pos)
    

    def move(self, target_pos):
        # distance to move is the distance from M to the target position
        # the robot's position is updated after the robot moves
        get_distance_to_move(self, target_pos)
        self.M = target_pos
        return self.M

   