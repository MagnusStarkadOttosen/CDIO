from src.mainloop import MainLoop

turnSpeed = 3
ml = MainLoop()
ml.initialize_field()
# ml.start_main_lo
ml.client_pc.send_command("max_speed")
