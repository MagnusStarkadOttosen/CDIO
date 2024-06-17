import logging


logging.basicConfig(filename='safe_detect_balls.log', filemode='w',
                    format='%(asctime)s - %(message)s')

logging.warning("This is logged.")

logging.warning("This is also logged.")
