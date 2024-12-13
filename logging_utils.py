from datetime import datetime

LOG_FILE = "user_activity.log"

def log_user_activity(username, action):
    """
    Logs user activity with a timestamp, username, and action.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {username} - {action}\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

def read_user_logs():
    """
    Reads the logs from the log file.
    """
    try:
        with open(LOG_FILE, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []
