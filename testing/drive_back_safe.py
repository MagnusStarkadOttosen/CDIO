from src.mainloop import MainLoop

turnSpeed = 3
ml = MainLoop()
ml.initialize_field()
# ml.start_main_loop()
ml.client_pc.send_command("drive_back_save -10 -5")
