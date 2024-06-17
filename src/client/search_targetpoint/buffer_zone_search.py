

def buffer_zone_search(ball_dot, i, j):
    target_point = [0][0]
    if i < 120:
        target_point = ball_dot[i][j + 270]
        return target_point
    elif i > 1080:
        target_point = ball_dot[i][j - 270]
        return target_point
    elif j < 120:
        target_point = ball_dot[i + 270][j]
        return target_point
    elif j > 1680:
        target_point = ball_dot[i - 270][j]
        return target_point
    return target_point
def is_ball_in_buffer_zone(ball_dot, i, j):
    if i < 120 or i > 1080 or j < 120 or j > 1680:
        return True
    return False