from src.client.field.buffer_zone import is_within_buffer_zone
from src.mainloop import MainLoop

robot_position_1 = [(60, 40)]
robot_position_2 = [(180, 190)]

main_loop = MainLoop()
main_loop.initialize_field()

main_loop.client.send_command("start_drive")
print("start_drive command sent")
# main_loop._navigate_to_target(robot_position_1)
# print("is within navigate to target zone")
# if is_within_buffer_zone(robot_position_1):
#         print("is within buffer zone")
#         main_loop.client.send_command("stop")
#         main_loop.client.send_command("move -20")
#         main_loop.client.send_command("stop")
# else:
#     main_loop.client.send_command("stop")

main_loop._navigate_to_target(robot_position_2)
if is_within_buffer_zone(robot_position_2):
        main_loop.client.send_command("stop")
        main_loop.client.send_command("move -20")
        main_loop.client.send_command("stop")
else:
    main_loop.client.send_command("stop")