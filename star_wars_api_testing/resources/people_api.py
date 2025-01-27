#resource/people_api.py
# People resource object
from typing import Dict, Any, List
import logging

class PeopleAPI:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def get_person(self, person_id: str) -> Dict[str, Any]:
       
        self.logger.info(f"Fetching person with ID: {person_id}")
        return self.client.get(f"people/{person_id}")
    
    def get_films(self, person_id: str) -> List[str]:
        """Get all films a person appears in"""
        person_data = self.get_person(person_id)
        return person_data.get('films', [])
    
    def get_species(self, person_id: str) -> List[str]:
        """Get species of a person"""
        person_data = self.get_person(person_id)
        return person_data.get('species', [])
    
    def get_vehicles(self, person_id: str) -> List[str]:
        """Get vehicles associated with a person"""
        person_data = self.get_person(person_id)
        return person_data.get('vehicles', [])
    
    def get_starships(self, person_id: str) -> List[str]:
        """Get starships associated with a person"""
        person_data = self.get_person(person_id)
        return person_data.get('starships', [])
    
    def get_homeworld(self, person_id: str) -> str:
        """Get person's homeworld"""
        person_data = self.get_person(person_id)
        return person_data.get('homeworld', '')