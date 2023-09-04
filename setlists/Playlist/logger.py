import datetime

class Logger:
    def __init__(self, log_file: str):
        """
        Initializes the Logger with the log file path.
        """
        self.log_file = log_file

    def log_error(self, error_message: str) -> None:
        """
        Logs an error message to the log file.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{timestamp}] {error_message}\n")
