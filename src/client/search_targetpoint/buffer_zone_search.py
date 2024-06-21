

def buffer_zone_search(ball_dot):
    target_point = (0,0)
    ball_x, ball_y = ball_dot
    if ball_x < 120:
        target_point = (ball_x,ball_y+ 270)
        return target_point
    elif ball_x > 1080:
        target_point = (ball_x,ball_y- 270)
        return target_point
    elif ball_y < 120:
        target_point = (ball_x+ 270,ball_y)
        return target_point
    elif ball_y > 1680:
        target_point = (ball_x- 270,ball_y)
        return target_point
    return target_point
def is_ball_in_buffer_zone(ball_dot):
    ball_x, ball_y = ball_dot
    if ball_x < 120 or ball_x > 1080 or ball_y < 120 or ball_y > 1680:
        return True
    return False