def corners_search(ball_dot,i,j):
    target_point = [0, 0]
    if i < 100 and j< 100:
        if i< j:
            target_point = [100, 100]
        else:
            target_point = [100, 100]
    elif i < 100 and j> 1100:
        target_point = [100, 1100]
    elif i>1700 and j< 100:
        target_point = [1700, 100]
    elif i > 1700 and j>1100:
        target_point = [1700, 1100]
   
def is_ball_in_corners(ball_dot, i, j):
    if i < 100 and j< 100 or i < 100 and j> 1100 or i>1700 and j< 100 or i > 1700 and j>1100: 
        return True