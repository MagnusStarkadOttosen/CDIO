from src.client.field.coordinate_system import warp_perspective
from src.client.vision.shape_detection import detect_robot
from src.mainloop import MainLoop
DST_SIZE = (1200, 1800)
PIVOT_POINTS = [(300, 600), (1500, 600)]
main_loop = MainLoop()

ret, frame = main_loop.camera.read()
warped_img = warp_perspective(frame, main_loop.final_points, DST_SIZE)

robot_pos, robot_direction = detect_robot(warped_img, main_loop.direction_color, main_loop.orange)
print(f"robot_pos: {robot_pos}, robot_direction: {robot_direction}")
main_loop.client.send_command("start_collect")
while robot_pos[1] < 600:

    main_loop.client.send_command("drive_back")
main_loop.client.send_command("stop")
main_loop.client.send_command("stop_collect")
print(f"Pivot point: {robot_pos}")