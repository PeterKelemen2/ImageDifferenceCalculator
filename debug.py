"""
logger.py - Simple Logger Module

This module provides a basic logging functionality to log messages with timestamps to a text file
and also print them to the standard error stream. The log file is stored in a 'logs' directory,
and each session is saved in a separate log file with a timestamp in the filename.

Usage:
    1. Import the module using: `from logger import log`
    2. Use the `log` function to log messages.

Example:
    from logger import log

    log("This is a log message.")

"""

from datetime import datetime
import sys
import os

# Global variables for logging
log_file_path = ""
log_folder_path = "logs"
session_started = False


def init_logger():
    """
    Initializes the logger by creating the 'logs' directory and setting up a new log file
    with a timestamp in the filename.
    """
    os.makedirs(log_folder_path, exist_ok=True)

    global log_file_path
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = f"{log_folder_path}/log_{date}.txt"

    global session_started
    session_started = True


def log(message):
    """
    Logs a message with a timestamp to both a text file and the standard output stream.

    Args:
        message (str): The message to be logged.

    Note:
        If a session is not already started, it initializes the logger before logging the message.
    """
    if session_started:
        date = datetime.now().strftime("[%Y.%m.%d - %H:%M:%S] ")
        with open(log_file_path, 'a') as log_file:
            log_file.write(date + str(message) + '\n')

        print("[Debug]" + date + str(message), file=sys.stdout)
    else:
        init_logger()
        log(message)
