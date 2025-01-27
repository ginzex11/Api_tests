# core/logger.py
import logging
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from colorama import Fore, Style, init
from star_wars_api_testing.config.test_config import TestConfig

init(autoreset=True)

class TestLogger:
    """Custom logger for test documentation and result tracking"""
    
    def __init__(self, name: str = "SWAPI Tests"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._configure_handlers()
        self.test_cases = []
        self.current_test = {}

    def _configure_handlers(self):
        """Configure logging handlers"""
        TestConfig.LOG_DIR.mkdir(parents=True, exist_ok=True)

        #JSON file handler
        file_handler = logging.FileHandler(TestConfig.LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(StructuredFormatter())

        #console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(ColoredFormatter())

        
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def start_test(self, test_name: str, description: str):
        """Log test start with documentation"""
        self.current_test = {
            "test_name": test_name,
            "description": description,
            "start_time": datetime.utcnow().isoformat(),
            "steps": []
        }
        self.logger.info(f"\n{Fore.YELLOW}Starting test: {test_name}")
        self.logger.info(f"{Fore.CYAN}Description: {description}")

    def log_step(self, step: str, expected: str, actual: Any, status: str):
        """Log individual test validation step"""
        step_details = {
            "step": step,
            "expected": expected,
            "actual": str(actual),
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.current_test["steps"].append(step_details)
        
        # Color coding 
        color = Fore.GREEN if status == "PASS" else Fore.RED
        self.logger.info(
            f"{color}• {step}\n"
            f"   Expected: {expected}\n"
            f"   Actual:   {actual}"
        )

    def end_test(self, status: str):
        """Log test completion with summary"""
        self.current_test.update({
            "end_time": datetime.utcnow().isoformat(),
            "status": status
        })
        self.test_cases.append(self.current_test)
        
        summary = (
            f"{Fore.YELLOW}Test completed: {self.current_test['test_name']}\n"
            f"{Fore.CYAN}Status: {status}\n"
            f"Steps executed: {len(self.current_test['steps'])}"
        )
        self.logger.info(summary)

    def save_report(self):
        """Save test report"""
        report = {
            "test_run_date": datetime.utcnow().isoformat(),
            "test_cases": self.test_cases
        }
        TestConfig.RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TestConfig.RESULTS_FILE, 'w') as f:
            json.dump(report, f, indent=2)

class StructuredFormatter(logging.Formatter):
    """JSON-structured logging """
    def format(self, record):
        return json.dumps(record.__dict__)

class ColoredFormatter(logging.Formatter):
    """colored output"""
    COLORS = {
        'INFO': Fore.CYAN,
        'DEBUG': Fore.BLUE,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, Fore.WHITE)
        return f"{color}{record.getMessage()}{Style.RESET_ALL}"