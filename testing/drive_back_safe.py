from src.mainloop import MainLoop
from src.client.field.coordinate_system import are_points_close,distance_left
import numpy as np

turnSpeed = 3
robot=(0,300)
MAXSPEED=30

def calc():
    distance = distance_left(robot,300)
    pace = np.round(distance/800)*MAXSPEED
    print(pace)
calc()

