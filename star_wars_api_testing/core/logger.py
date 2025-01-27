# Logging configuration
# core/logger.py
import logging
from config.test_config import TestConfig

def setup_logger():
    TestConfig.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        filename=TestConfig.LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console_handler)
