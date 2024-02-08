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
log_file = None
log_file_path = ""
log_folder_path = "logs"
session_started = False
last_timestamp = None


def init_logger():
    """
    Initializes the logger by creating the 'logs' directory and setting up a new log file
    with a timestamp in the filename.
    """
    os.makedirs(log_folder_path, exist_ok=True)

    global log_file
    global log_file_path
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = f"{log_folder_path}/log_{date}.txt"
    log_file = open(log_file_path, "a")

    global session_started
    session_started = True


def get_current_timestamp():
    """
    Returns the current timestamp formatted as "[%Y.%m.%d - %H:%M:%S]".

    Note:
        This function caches the formatted timestamp and returns the cached value if
        it was generated within the same second.
    """
    global last_timestamp
    current_time = datetime.now()
    if last_timestamp is None or current_time.second != last_timestamp.second:
        last_timestamp = current_time  # Store datetime object
    return last_timestamp.strftime("[%Y.%m.%d - %H:%M:%S] ")  # Format when returning


def log(message):
    """
    Logs a message with a timestamp to both a text file and the standard output stream.

    Args:
        message (str): The message to be logged.

    Note:
        If a session is not already started, it initializes the logger before logging the message.
    """
    global log_file
    if not session_started:
        init_logger()

    timestamp = get_current_timestamp()
    date = datetime.now().strftime("[%Y.%m.%d - %H:%M:%S] ")
    log_message = "[Debug]" + timestamp + str(message)
    log_file.write(log_message + '\n')  # Write message to log file
    log_file.flush()  # Flush buffer to ensure message is written immediately
    print(log_message, file=sys.stdout)  # Print message to stdout
