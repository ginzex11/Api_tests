import csv
import logging
from typing import List, Dict, Any
from config.test_config import TestConfig

class TestDataHandler:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.required_fields = ['person_id', 'film_id']
    
    def load_test_data(self) -> List[Dict[str, Any]]:
        """
        Load and validate test data from CSV file, skipping comment lines
        
        Returns:
            List of validated test cases
        """
        self.logger.info(f"Loading test data from {TestConfig.TEST_DATA_FILE}")
        valid_test_cases = []
        
        try:
            with open(TestConfig.TEST_DATA_FILE, 'r', encoding='utf-8') as f:
                # Skip comment line
                for line in f:
                    if not line.startswith('#'):
                        break
                
                # Read CSV data
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        cleaned_case = {
                            'person_id': str(row['person_id']).strip(),
                            'film_id': str(row['film_id']).strip(),
                            'planet_id': str(row['planet_id']).strip(),
                            'notes': str(row['notes']).strip()
                        }
                        
                        # Validate required fields
                        if all(cleaned_case[field] for field in self.required_fields):
                            valid_test_cases.append(cleaned_case)
                            self.logger.debug(f"Valid test case found: {cleaned_case}")
                        else:
                            self.logger.warning(f"Invalid test case at row {row_num}: Missing required fields")
                            
                    except KeyError as e:
                        self.logger.warning(f"Missing column in row {row_num}: {str(e)}")
                    except Exception as e:
                        self.logger.warning(f"Error processing row {row_num}: {str(e)}")
            
            self.logger.info(f"Successfully loaded {len(valid_test_cases)} valid test cases")
            
            if not valid_test_cases:
                self.logger.error("No valid test cases found in the data file!")
            
            return valid_test_cases
            
        except FileNotFoundError:
            self.logger.error(f"Test data file not found: {TestConfig.TEST_DATA_FILE}")
            return []
        except Exception as e:
            self.logger.error(f"Error loading test data: {str(e)}")
            return []
    
    def save_results(self, results: List[Dict[str, Any]]) -> None:
        """
        Save test results to CSV file
        
        Args:
            results: List of test results to save
        """
        if not results:
            self.logger.warning("No results to save")
            return
        
        try:
            TestConfig.RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(TestConfig.RESULTS_FILE, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['test_case', 'status', 'details', 'timestamp']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
                
            self.logger.info(f"Successfully saved {len(results)} test results to {TestConfig.RESULTS_FILE}")
            
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise