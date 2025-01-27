# Cross-reference tests
# tests/test_cross_reference.py
import pytest
from resources.people_api import PeopleAPI
from resources.films_api import FilmsAPI
from utils.data_handler import TestDataHandler
from core.api_client import SwapiClient
import logging

class TestCrossReference:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = SwapiClient()
        self.people_api = PeopleAPI(self.client)
        self.films_api = FilmsAPI(self.client)
        self.data_handler = TestDataHandler()
        self.results = []
        self.logger = logging.getLogger(__name__)
    
    def test_people_films_cross_reference(self):
        """
        Test case 1: Cross-reference between people and films
        Verifies that if a person appears in a film's characters,
        that film also appears in the person's films list
        """
        test_cases = self.data_handler.load_test_data()
        
        for test_case in test_cases:
            person_id = test_case['person_id']
            expected_film_id = test_case['film_id']
            
            try:
                # Step 1: Get person's films
                person_data = self.people_api.get_person(person_id)
                person_films = person_data['films']
                
                # Step 2: Get film's characters
                film_data = self.films_api.get_film(expected_film_id)
                film_characters = film_data['characters']
                
                # Step 3: Cross-reference validation
                person_url = f"{self.client.base_url}/people/{person_id}/"
                film_url = f"{self.client.base_url}/films/{expected_film_id}/"
                
                # Verify film in person's films
                assert film_url in person_films, \
                    f"Film {expected_film_id} not found in person {person_id}'s films"
                
                # Verify person in film's characters
                assert person_url in film_characters, \
                    f"Person {person_id} not found in film {expected_film_id}'s characters"
                
                self.results.append({
                    'test_case': f"Cross-reference Person {person_id} - Film {expected_film_id}",
                    'status': 'PASS',
                    'details': 'Successfully validated cross-reference'
                })
                
            except Exception as e:
                self.logger.error(f"Test failed for person {person_id} and film {expected_film_id}: {str(e)}")
                self.results.append({
                    'test_case': f"Cross-reference Person {person_id} - Film {expected_film_id}",
                    'status': 'FAIL',
                    'details': str(e)
                })
    
    def test_planets_residents_cross_reference(self):
        """
        Test case 2: Cross-reference between planets and their residents
        Verifies that if a person is listed as a resident of a planet,
        that planet is also listed as their homeworld
        """
        test_cases = self.data_handler.load_test_data()
        
        for test_case in test_cases:
            planet_id = test_case.get('planet_id')
            if not planet_id:  # Skip if no planet_id in test case
                continue
                
            try:
                # Step 1: Get planet's residents
                planet_data = self.planets_api.get_planet(planet_id)
                planet_residents = planet_data['residents']
                
                for resident_url in planet_residents:
                    resident_id = resident_url.split('/')[-2]
                    
                    # Step 2: Get resident's homeworld
                    resident_data = self.people_api.get_person(resident_id)
                    resident_homeworld = resident_data['homeworld']
                    
                    # Step 3: Verify cross-reference
                    planet_url = f"{self.client.base_url}/planets/{planet_id}/"
                    assert resident_homeworld == planet_url, \
                        f"Planet {planet_id} not listed as homeworld for resident {resident_id}"
                    
                    self.results.append({
                        'test_case': f"Planet-Resident Cross-reference: Planet {planet_id} - Resident {resident_id}",
                        'status': 'PASS',
                        'details': 'Successfully validated planet-resident relationship'
                    })
                    
            except Exception as e:
                self.logger.error(f"Test failed for planet {planet_id}: {str(e)}")
                self.results.append({
                    'test_case': f"Planet-Resident Cross-reference: Planet {planet_id}",
                    'status': 'FAIL',
                    'details': str(e)
                })
    
    def teardown_method(self, method):
        """Save test results after each test method"""
        self.data_handler.save_results(self.results)