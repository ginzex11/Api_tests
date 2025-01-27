# Films resource object
#recourse/films_api.py
from typing import Dict, Any, List
import logging

class FilmsAPI:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def get_film(self, film_id: str) -> Dict[str, Any]:
        
        self.logger.info(f"Fetching film with ID: {film_id}")
        return self.client.get(f"films/{film_id}")
    
    def get_characters(self, film_id: str) -> List[str]:
        """Get all characters in a film"""
        film_data = self.get_film(film_id)
        return film_data.get('characters', [])
    
    def get_planets(self, film_id: str) -> List[str]:
        """Get all planets in a film"""
        film_data = self.get_film(film_id)
        return film_data.get('planets', [])
    
    def get_starships(self, film_id: str) -> List[str]:
        """Get all starships in a film"""
        film_data = self.get_film(film_id)
        return film_data.get('starships', [])
    
    def get_vehicles(self, film_id: str) -> List[str]:
        """Get all vehicles in a film"""
        film_data = self.get_film(film_id)
        return film_data.get('vehicles', [])
    
    def get_species(self, film_id: str) -> List[str]:
        """Get all species in a film"""
        film_data = self.get_film(film_id)
        return film_data.get('species', [])