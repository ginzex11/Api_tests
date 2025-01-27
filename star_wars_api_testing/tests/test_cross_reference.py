# tests/test_cross_reference.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from star_wars_api_testing.core.logger import TestLogger
import pytest
from datetime import datetime
from star_wars_api_testing.resources.resource_factory import ResourceFactory
from star_wars_api_testing.utils.data_handler import DataHandler
from star_wars_api_testing.core.api_client import SwapiClient
import logging
import time  

class TestCrossReference:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = SwapiClient()
        self.resources = ResourceFactory(self.client)
        self.data_handler = DataHandler()
        self.logger = TestLogger(__name__)
        self.results = []

    def test_people_films_cross_reference(self):
        """Validate character-film cross-references"""
        test_cases = self.data_handler.load_test_data()
        
        self.logger.start_test(
            test_name="Character-Film Cross-Reference Validation",
            description="Verify characters appear in specified films and vice versa"
        )

        for test_case in test_cases:
            test_identifier = f"Person {test_case['person_id']} - Film {test_case['film_id']}"
            
            try:
                # Test execution
                person_films = self.resources.people.get_films(test_case['person_id'])
                film_characters = self.resources.films.get_characters(test_case['film_id'])

                # Validation steps
                self.logger.log_step(
                    step=f"{test_identifier}: Film in character's list",
                    expected=f"Film {test_case['film_id']} should be present",
                    actual=f"Found {len(person_films)} films",
                    status="PASS" if str(test_case['film_id']) in person_films else "FAIL"
                )

                self.logger.log_step(
                    step=f"{test_identifier}: Character in film's cast",
                    expected=f"Character {test_case['person_id']} should be present",
                    actual=f"Found {len(film_characters)} characters",
                    status="PASS" if str(test_case['person_id']) in film_characters else "FAIL"
                )

            except Exception as e:
                self.logger.log_step(
                    step=test_identifier,
                    expected="Successful API response",
                    actual=str(e),
                    status="ERROR"
                )

        self.logger.end_test(status="COMPLETED")
        self.logger.save_report()
    
    def teardown_method(self, method):
        """Save test results after each test method"""
        if self.results:
            try:
                self.data_handler.save_results(self.results)
            except Exception as e:
                self.logger.error(f"Failed to save test results: {str(e)}")
