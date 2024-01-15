from datetime import datetime
import sys
import os

log_file_path = ""
log_folder_path = "logs"

session_started = False


def init_logger():
    os.makedirs(log_folder_path, exist_ok=True)

    global log_file_path
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = f"{log_folder_path}/log_{date}.txt"

    global session_started
    session_started = True


def log(message):
    if session_started:
        date = datetime.now().strftime("[%Y.%m.%d - %H:%M:%S] ")
        with open(log_file_path, 'a') as log_file:
            log_file.write(date + str(message) + '\n')

        print("[Debug]" + date + str(message), file=sys.stderr)
    else:
        init_logger()
        log(message)
