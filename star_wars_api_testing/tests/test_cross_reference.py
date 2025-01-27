import pytest
from datetime import datetime
from resources.resource_factory import ResourceFactory
from utils.data_handler import TestDataHandler
from core.api_client import SwapiClient
import logging

class TestCrossReference:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = SwapiClient()
        self.resources = ResourceFactory(self.client)  # Use ResourceFactory
        self.data_handler = TestDataHandler()
        self.results = []
        self.logger = logging.getLogger(__name__)
    
    def test_people_films_cross_reference(self):
        """
        Test case 1: Cross-reference between people and films
        """
        test_cases = self.data_handler.load_test_data()
        
        if not test_cases:
            self.logger.error("No valid test cases found. Skipping tests.")
            pytest.skip("No valid test cases available")
        
        for test_case in test_cases:
            try:
                person_id = test_case['person_id']
                film_id = test_case['film_id']
                test_identifier = f"Person {person_id} - Film {film_id}"
                
                self.logger.info(f"Testing cross-reference for {test_identifier}")
                
                # Use resource factory to get data
                person_films = self.resources.people.get_films(person_id)
                film_characters = self.resources.films.get_characters(film_id)
                
                expected_film_url = f"{self.client.base_url}/films/{film_id}/"
                expected_person_url = f"{self.client.base_url}/people/{person_id}/"
                
                # Validate cross-references
                film_in_person = expected_film_url in person_films
                person_in_film = expected_person_url in film_characters
                
                if film_in_person and person_in_film:
                    status = "PASS"
                    details = "Successfully validated cross-reference"
                else:
                    status = "FAIL"
                    details = f"Cross-reference mismatch: film_in_person={film_in_person}, person_in_film={person_in_film}"
                
                self.results.append({
                    'test_case': test_identifier,
                    'status': status,
                    'details': details,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                self.logger.error(f"Test failed: {str(e)}")
                self.results.append({
                    'test_case': test_identifier if 'test_identifier' in locals() else "Unknown test case",
                    'status': 'ERROR',
                    'details': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    def teardown_method(self, method):
        """Save test results after each test method"""
        if self.results:
            try:
                self.data_handler.save_results(self.results)
            except Exception as e:
                self.logger.error(f"Failed to save test results: {str(e)}")