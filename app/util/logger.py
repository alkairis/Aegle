import logging
import os


class Logger:
    _conigured = False
    
    def __init__(self, name, log_file_path=None, log_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        if not Logger._conigured:
            self.setup_logging()
            Logger._conigured = True

    def setup_logging(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "resource/gcp-serviceaccount.json"
        client = Client()
        handler = CloudLoggingHandler(client, transport=BackgroundThreadTransport)
        
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
            
        logging.getLogger().handlers = []
        logging.getLogger().addHandler(handler)
        setup_logging(handler)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.info(message)
        
class Logger:
    """
        Initializes a Logger instance with a specified name, log file path, and log level.

        This constructor sets up a logger with the given name and log level, clears any
        existing handlers to prevent duplicate logs, and configures logging to a specified
        file path.

        Args:
            logger_name (str): The name of the logger.
            log_file_path (str): The file path where logs will be stored.
            log_level (int, optional): The logging level, default is logging.DEBUG.
        """

    def __init__(self, logger_name, log_file_path="logs/medical-bot.log", log_level=logging.DEBUG):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        # Clear existing handlers to prevent duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.setup_logging(log_file_path)

    def setup_logging(self, log_file_path):
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        # File Handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.info(message)

    def log(self, level, message):
        self.logger.log(level, message)
