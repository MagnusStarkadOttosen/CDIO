from client.vision.shape_detection import detect_obstacles

def obstacle_Search(ball_dot, i, j, midpoint):
    target_point = [0, 0]
    if ball_dot[i] < midpoint[i] and ball_dot[j] < midpoint[j]:
        target_point = [midpoint[0] - 90, midpoint[1] - 270]     
    elif ball_dot[i] < midpoint[i] and ball_dot[j] > midpoint[j]:
        target_point = [midpoint[0] - 90, midpoint[1] + 270]       
    elif ball_dot[i] > midpoint[i] and ball_dot[j] > midpoint[j]:
        target_point = [midpoint[0] + 90, midpoint[1] - 270]        
    elif ball_dot[i] > midpoint[i] and ball_dot[j] < midpoint[j]:
        target_point = [midpoint[0] + 90, midpoint[1] + 270]      
    return target_point

   
    