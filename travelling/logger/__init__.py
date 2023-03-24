from datetime import datetime
import logging
import os
from datetime import datetime
import pandas as pd

LOG_DIR= "travel_logs"

CURRENT_TIME_STEMP= f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"

log_file_name= f"log{CURRENT_TIME_STEMP}.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_file_path= os.path.join(LOG_DIR,log_file_name)

logging.basicConfig(filename=log_file_path,
filemode="w",
#format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
level=logging.INFO
)

