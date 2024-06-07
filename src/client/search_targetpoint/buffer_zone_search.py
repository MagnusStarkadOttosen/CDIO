

def buffer_zone_search(ball_dot, i, j):
    target_point = [0][0]
    if i < 100:
        target_point = ball_dot[i][j + 250]
        return target_point
    elif i > 1100:  
        target_point = ball_dot[i][j - 250]
        return target_point
    elif j < 100:
        target_point = ball_dot[i + 250][j]
        return target_point
    elif j > 1700:
        target_point = ball_dot[i - 250][j]
        return target_point
    return target_point

   