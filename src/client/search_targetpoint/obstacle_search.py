# from client.vision.shape_detection import detect_obstacles

def obstacle_Search(ball_dot, midpoint):
    target_point = (0,0)
    target = (0,0)
    if ball_dot[0] < midpoint[0] and ball_dot[1] < midpoint[1]:
        target_point = [midpoint[0] - 95, midpoint[1] - 320]  
        target=   [midpoint[0] - 85, midpoint[1] + 300]  
    elif ball_dot[0] < midpoint[0] and ball_dot[1] > midpoint[1]:
        target_point = [midpoint[0] - 95, midpoint[1] + 320]  
        target=   [midpoint[0] - 85, midpoint[1] - 300]     
    elif ball_dot[0] > midpoint[0] and ball_dot[1] > midpoint[1]:
        target_point = [midpoint[0] + 95, midpoint[1] - 320] 
        target=   [midpoint[0] + 85, midpoint[1] + 300]       
    elif ball_dot[0] > midpoint[0] and ball_dot[1] < midpoint[1]:
        target_point = [midpoint[0] + 95, midpoint[1] + 320]   
        target=   [midpoint[0] + 85, midpoint[1] - 300]   
    return target_point, target

def is_ball_in_obstacle(ball_dot, midpoint):
    print(f"ball_coords: {ball_dot} midpoint: {midpoint}")
    if(abs(ball_dot[0]-midpoint[0])<100 and abs(ball_dot[1]-midpoint[1])<100):
        target_point = obstacle_Search(ball_dot, midpoint)
        target = obstacle_Search(ball_dot, midpoint)
        return True, target_point, target
    return False, None, None
    

    