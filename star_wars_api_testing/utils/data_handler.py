# Test data handling utilities
# utils/data_handler.py
import csv
import logging
from typing import List, Dict, Any
from config.test_config import TestConfig

class TestDataHandler:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def load_test_data(self) -> List[Dict[str, Any]]:
        TestConfig.TEST_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Loading test data from {TestConfig.TEST_DATA_FILE}")
        
        test_cases = []
        try:
            with open(TestConfig.TEST_DATA_FILE, 'r') as f:
                reader = csv.DictReader(f)
                test_cases = list(reader)
            self.logger.info(f"Loaded {len(test_cases)} test cases")
            return test_cases
        except Exception as e:
            self.logger.error(f"Error loading test data: {str(e)}")
            raise
    
    def save_results(self, results: List[Dict[str, Any]]):
        TestConfig.RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Saving results to {TestConfig.RESULTS_FILE}")
        
        try:
            with open(TestConfig.RESULTS_FILE, 'w', newline='') as f:
                writer = csv.DictWriter(f, 
                    fieldnames=['test_case', 'status', 'details'])
                writer.writeheader()
                writer.writerows(results)
            self.logger.info(f"Saved {len(results)} test results")
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise