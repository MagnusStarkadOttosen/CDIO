import math

WHEEL_DIMENSION = 80
WHEEL_CIRCUMF_CM = WHEEL_DIMENSION * math.pi


def get_distance_to_move(robot_pos, target_pos):
    print(f"robot pos :  {robot_pos} and target_pos :  {target_pos}")
    dist_vector = robot_pos - target_pos
    distance = round(math.sqrt(dist_vector[0] ** 2 + dist_vector[1] ** 2), 1)
    return distance

def get_degrees_to_pivot(robot_pos: Pos, target_pos: Pos):

    dist_x = robot_pos.x - target_pos.x
    dist_y = robot_pos.y - target_pos.y
    angle = math.degrees(math.atan2(dist_y, dist_x))
    return angle


def get_distance_to_move(self, target_pos):
        b = math.sqrt((target_pos[0] - self.M[0]) ** 2 + (target_pos[1] - self.M[1]) ** 2)
        return b


# calculate the degrees between the vector MB and the vector MC
def get_degrees_toturn(self, target_pos):
         # distance MB = a
        a = math.sqrt((self.B[0] - self.M[0]) ** 2 + (self.B[1] - self.M[1]) ** 2)
        # distance MC = b
        b = math.sqrt((target_pos[0] - self.M[0]) ** 2 + (target_pos[1] - self.M[1]) ** 2)
        # distance BC = c
        c = math.sqrt((target_pos[0] - self.B[0]) ** 2 + (target_pos[1] - self.B[1]) ** 2)
        #radian of angle between vector MB and vector MC
        radian = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
        #degrees of angle between vector MB and vector MC
        degrees = math.degrees(radian)
        return degrees