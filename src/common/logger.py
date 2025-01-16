import os.path
import logging
import sys
from datetime import datetime

class LoggerWriter:
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self.buffer = ""

    def write(self, message):
        if message.strip():
            self.logger.log(self.log_level, message.strip())

    def flush(self):
        pass

class LoggerManager:
    def __init__(self, log_file_path, disabledConsole) -> None:
        log_filename = os.path.join(log_file_path, f"{datetime.now().strftime('%Y_%m_%d_%H')}.log")
        handlers = [logging.FileHandler(log_filename)]
        
        if not disabledConsole:
            handlers.append(logging.StreamHandler(sys.stdout))
        
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=handlers
        )
        self.logger = logging.getLogger(str("Elyon"))

        sys.stdout = LoggerWriter(self.logger, logging.INFO)
        sys.stderr = LoggerWriter(self.logger, logging.ERROR)
    
    def __call__(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def critical(self, message):
        self.logger.critical(message)
    
    def exception(self, message):
        self.logger.exception(message)
