# tests/test_custom.py
import pytest
from datetime import datetime
from star_wars_api_testing.resources.resource_factory import ResourceFactory
from star_wars_api_testing.utils.data_handler import DataHandler
from star_wars_api_testing.core.api_client import SwapiClient
import logging

class TestPlanetResidents:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = SwapiClient()
        self.resources = ResourceFactory(self.client)
        self.data_handler = DataHandler()
        self.results = []
        self.logger = logging.getLogger(__name__)
    
    def test_planet_residents_cross_reference(self):
        """
        Test case 2: Cross-reference between planets and their residents
        Verifies that if a person is listed as a resident of a planet,
        that planet is also listed as their homeworld
        """
        test_cases = self.data_handler.load_test_data()
        
        if not test_cases:
            self.logger.error("No valid test cases found. Skipping tests.")
            pytest.skip("No valid test cases available")
        
        for test_case in test_cases:
            try:
                person_id = test_case['person_id']
                planet_id = test_case['planet_id']
                test_identifier = f"Person {person_id} - Planet {planet_id}"
                
                self.logger.info(f"Testing planet-resident cross-reference for {test_identifier}")
                
                # Get planet residents and person's homeworld
                planet_residents = self.resources.planets.get_residents(planet_id)
                person_homeworld = self.resources.people.get_homeworld(person_id)
                
                expected_person_url = f"{self.client.base_url}/people/{person_id}/"
                expected_planet_url = f"{self.client.base_url}/planets/{planet_id}/"
                
                # Validate cross-references
                person_in_residents = expected_person_url in planet_residents
                planet_is_homeworld = person_homeworld == expected_planet_url
                
                if person_in_residents and planet_is_homeworld:
                    status = "PASS"
                    details = "Successfully validated planet-resident cross-reference"
                else:
                    status = "FAIL"
                    details = (f"Cross-reference mismatch: person_in_residents={person_in_residents}, "
                             f"planet_is_homeworld={planet_is_homeworld}")
                
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