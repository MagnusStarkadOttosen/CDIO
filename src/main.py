import sys

from src.mainloop import MainLoop

ml = MainLoop()
# with open("output.txt", "w") as f:
#     sys.stdout = f
ml.start_main_loop()

# sys.stdout = sys.__stdout__


