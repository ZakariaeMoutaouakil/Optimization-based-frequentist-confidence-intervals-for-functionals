import logging

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ColorFormatter(logging.Formatter):
    """
    Custom logging formatter to add colors based on log levels.
    """

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record as text with colors based on the log level.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record.
        """
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        levelname = f"{record.levelname:<8}"  # Left align and pad the level name to 8 characters
        record.msg = f"{log_color}{levelname} - {record.msg}{Style.RESET_ALL}"
        return super().format(record)


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """
    Set up a logger with specified name and log file.

    Args:
        name (str): The name of the logger.
        log_file (str): The file path for the log file.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(levelname)-8s - %(message)s')
        file_handler.setFormatter(file_format)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        color_format = ColorFormatter('%(message)s')
        console_handler.setFormatter(color_format)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
