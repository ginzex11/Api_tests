# utils/data_handler.py
import csv
import logging
from typing import List, Dict, Any
from star_wars_api_testing.config.test_config import TestConfig

class DataHandler:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.required_fields = ['person_id', 'film_id']

    def load_test_data(self) -> List[Dict[str, Any]]:
        
        self.logger.info(f"Loading test data from {TestConfig.TEST_DATA_FILE}")
        self.logger.info(f"Absolute path: {TestConfig.TEST_DATA_FILE.absolute()}")
        valid_test_cases = []

        try:
            with open(TestConfig.TEST_DATA_FILE, 'r', encoding='utf-8') as f:
                # Read all lines and skip comments
                lines = [line for line in f if not line.strip().startswith('#')]

                # Use the first line as the header
                reader = csv.DictReader(lines)

                # Log the columns found in the CSV file
                self.logger.debug(f"CSV columns: {reader.fieldnames}")

                for row_num, row in enumerate(reader, start=1):
                    try:
                        cleaned_case = {
                            'person_id': str(row['person_id']).strip(),
                            'film_id': str(row['film_id']).strip(),
                            'planet_id': str(row['planet_id']).strip(),
                            'notes': str(row['notes']).strip()
                        }

                        # Log the row being processed
                        self.logger.debug(f"Processing row {row_num}: {cleaned_case}")

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
    
        if not results:
            self.logger.warning("No results to save")
            return

        try:
            TestConfig.RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

            with open(TestConfig.RESULTS_FILE, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['test_case', 'status', 'details', 'timestamp', 'execution_time']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)

            self.logger.info(f"Successfully saved {len(results)} test results to {TestConfig.RESULTS_FILE}")

        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise