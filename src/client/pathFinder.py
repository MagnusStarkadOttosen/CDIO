from src.vision.shape_detection import Shapes,Pos
from src.vision.image_measurement import convert_px_cm
from src.vision.wheel_movement import  get_distance_to_move,np

class Route:
    def __init__(self, x, y,d,newAngle,drivingMode):
        self.x = x
        self.y = y
        self.d = d
        self.newAngle = newAngle
        self.drivingMode = drivingMode

def are_balls_remaining(shapes):
    if shapes.circles is not None:
        return True
    else:
        False

def findNearestBall(robotpostition:Pos,shape:Shapes,wallPosition:Route):
    nearest = 300
    circles = np.round(shape.circles[0, :]).astype("int")
    for (x, y,z) in circles:
        width_cm, height_cm = convert_px_cm(x, y)
        ball= Pos(width_cm,height_cm)
        dist=get_distance_to_move(robotpostition,ball)
        if(dist<nearest):
            wallPosition.x=x
            wallPosition.y=y
            wallPosition.d=dist
    return wallPosition

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
    if(wallPositon.d>=minWallDistance):
        roboDrive(route,pos,shape)

    else:
        straightDrive(route,pos,shape)






