from src.client.field.buffer_zone import is_within_buffer_zone
from src.mainloop import MainLoop

robot_position_1 = (640, 420)
robot_position_2 = (900, 100)

# Define a list of robot positions to test
robot_positions = [
    (50, 50),  # Outside, top-left
    (1000, 1100),  # Outside
    (180, 180),  # Outside
    (1650, 50),  # Outside, top-right
    (1650, 1050),  # Outside, bottom-right
    (50, 1050),  # Outside, bottom-left
    (500, 50),  # Outside, near top boundary
    (500, 1200),  # Outside, near bottom boundary
]

main_loop = MainLoop()
main_loop.initialize_field()

main_loop.client.send_command("start_drive")
print("start_drive command sent")

# Loop through each robot position and test it
for idx, position in enumerate(robot_positions, start=1):
    print("Check a new point:")
    print(f"Testing robot_position_{idx}: {position}")
    main_loop._navigate_to_target([position])
    if is_within_buffer_zone(position):
        print(f"Robot position {position} is within buffer zone")
        main_loop.client.send_command("stop")
        main_loop.client.send_command("drive_back")
        main_loop.client.send_command("stop")
    else:
        print(f"Robot position {position} is outside the buffer zone")
        main_loop.client.send_command("stop")
#
# main_loop._navigate_to_target([robot_position_1])
# print("is within navigate to target zone")
# if is_within_buffer_zone(robot_position_1):
#         print("is within buffer zone")
#         main_loop.client.send_command("stop")
#         main_loop.client.send_command("move -20")
#         main_loop.client.send_command("stop")
# else:
#     main_loop.client.send_command("stop")
#
# main_loop._navigate_to_target([robot_position_2])
# print("is within navigate to target zone in testing")
# if is_within_buffer_zone(robot_position_2):
#         print("is within buffer zone i main loop")
#         main_loop.client.send_command("stop")
#         # result = is_within_buffer_zone(robot_position_2)
#         # print(f"Robot position {robot_position_2} is outside the green rectangle: {result}")
#         main_loop.client.send_command("drive_back")
#         # main_loop.client.send_command("stop")
# else:
#     main_loop.client.send_command("stop")