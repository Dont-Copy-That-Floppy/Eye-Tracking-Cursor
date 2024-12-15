# logger.py
import logging


class Logger:
    """Sets up a centralized logger for the application."""

    @staticmethod
    def setup_logger(log_file="app.log", level=logging.INFO):
        """Configures the logger."""
        logging.basicConfig(filename=log_file, level=level, format="%(asctime)s - %(levelname)s - %(message)s")
        return logging.getLogger("EyeTrackingApp")


# Usage example:
# logger = Logger.setup_logger()
# logger.info("Application started.")
