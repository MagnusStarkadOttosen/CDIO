# from client.vision.shape_detection import detect_obstacles

def obstacle_Search(ball_dot, i, j, midpoint):
    target_point = [0, 0]
    if ball_dot[i] < midpoint[i] and ball_dot[j] < midpoint[j]:
        target_point = [midpoint[0] - 95, midpoint[1] - 320]  
        target=   [midpoint[0] - 95, midpoint[1] + 320]  
    elif ball_dot[i] < midpoint[i] and ball_dot[j] > midpoint[j]:
        target_point = [midpoint[0] - 95, midpoint[1] + 320]  
        target=   [midpoint[0] - 95, midpoint[1] - 320]     
    elif ball_dot[i] > midpoint[i] and ball_dot[j] > midpoint[j]:
        target_point = [midpoint[0] + 95, midpoint[1] - 320] 
        target=   [midpoint[0] + 95, midpoint[1] + 320]       
    elif ball_dot[i] > midpoint[i] and ball_dot[j] < midpoint[j]:
        target_point = [midpoint[0] + 95, midpoint[1] + 320]   
        target=   [midpoint[0] + 95, midpoint[1] - 320]   
    return target_point, target

def is_ball_in_obstacle(ball_dot, midpoint):
    print(f"ball_coords: {ball_dot} midpoint: {midpoint}")
    if(abs(ball_dot[0]-midpoint[0])<100 and abs(ball_dot[1]-midpoint[1])<100):
        target_point = obstacle_Search(ball_dot, 0, 1, midpoint)
        target = obstacle_Search(ball_dot, 0, 1, midpoint)
        return True, target_point, target
    return False, None, None
    

    