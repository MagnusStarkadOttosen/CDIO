# from src.vision.shape_detection import Shapes,Pos
import numpy as np

from src.vision.image_measurement import convert_px_cm
from src.vision.shape_detection import Shapes
from src.vision.wheel_movement import get_distance_to_move

class Pos:
    def __init__(self):
        self.x = 0
        self.y = 0
class Route:
    def __init__(self, x, y,d,newAngle,drivingMode):
        self.x = x
        self.y = y
        self.d = d
        self.newAngle = newAngle
        self.drivingMode = drivingMode

def balls_are_remaining(shapes):
    if shapes.circles is not None:
        return True
    else:
        return False


def findNearestBall(robotpostition, shape:Shapes):
    ball_route = Route(0, 0, 0, 0, " ")
    circles = np.round(shape.circles[0, :]).astype("int")
    if balls_are_remaining:
        nearest = 300000
        for (x, y, r) in circles:
            # width_cm, height_cm = convert_px_cm(circle.x, circle.y)
            # ball = np.array([width_cm, height_cm])
            # print(f"width : {width_cm} heigth: {height_cm}")
            dist=get_distance_to_move(robotpostition, np.array([x, y]))
            print("dist before if: ", dist)
            if(dist<nearest):
                ball_route.x=x
                ball_route.y=y
                ball_route.d=dist
                print("dist: ", dist)
                nearest=dist
        print(ball_route.d)
        return ball_route
    else:
        return 0

def findNearestWall(robotpostition:Pos,shape:Shapes,route:Route):
    nearest = 300
    lines = np.round(shape.lines[0, :]).astype("int")

    for (x, y,z) in lines:
        width_cm, height_cm = convert_px_cm(x, y)
        ball= Pos(width_cm,height_cm)
        dist=get_distance_to_move(robotpostition,ball)
        if(dist<nearest):
            route.x=x
            route.y=y
            route.d=dist

def roboDrive(route:Route,pos:Pos,shape:Shapes):
   findNearestBall(pos,shape,route)
   route.drivingmode="roboDrive"
   return route

def straightDrive(route:Route,pos:Pos,shape:Shapes):
    #angele=findAngle(robotPos,ballPos)
    #route.newAngle=angle
    findNearestBall(pos,shape,route)
    route.drivingmode="straightDrive"
    return route



def sendRoute(route:Route,pos:Pos,shape:Shapes,minWallDistance):
    wallPositon= Route(0,0,0,0,"")
    findNearestWall(wallPositon)
   # if(wallPositon.d>=minWallDistance):
   #     roboDrive(route,pos,shape)

   # else:
    straightDrive(route,pos,shape)
    return route






