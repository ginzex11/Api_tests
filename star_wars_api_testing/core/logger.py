# # Logging configuration
# # core/logger.py
# import logging
# from config.test_config import TestConfig

# def setup_logger():
#     TestConfig.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
#     logging.basicConfig(
#         filename=TestConfig.LOG_FILE,
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )
    
#     # Also log to console
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)
#     logging.getLogger('').addHandler(console_handler)
# core/logger.py

import logging
from config.test_config import TestConfig
import os

def setup_logger(name='test_logger'):
    # Ensure log directory exists
    TestConfig.LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Create a file handler for logging to a file
    log_file = os.path.join(TestConfig.LOG_DIR, TestConfig.LOG_FILE)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Log everything to file
    
    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)

    # Create console handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Log important messages to console

    # Create logger with the given name
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Overall logging level for this logger

    # Add the handlers to the logger
    if not logger.handlers:  # Prevent adding duplicate handlers if setup_logger is called multiple times
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # Return the logger so it can be used elsewhere
    return logger

# Example usage in your test scripts or modules:
# from core.logger import setup_logger
# logger = setup_logger('test_cross_reference')
# logger.debug("This is a debug message")
# logger.info("This is an info message")