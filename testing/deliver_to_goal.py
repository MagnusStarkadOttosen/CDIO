from src.mainloop import MainLoop
from testing.MoveAtoBVideo import client_pc

turnSpeed = 3
ml = MainLoop()
ml.initialize_field()
ml.start_main_loop()
ml._deliver_balls()
client_pc.send_command(f"turn_left {-turnSpeed}")
