#resource/planets_api.py
# Planets resource object
from typing import Dict, Any
import logging

class PlanetsAPI:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def get_planet(self, planet_id: str) -> Dict[str, Any]:
       
        self.logger.info(f"Fetching planet with ID: {planet_id}")
        return self.client.get(f"planets/{planet_id}")
    
    def get_residents(self, planet_id: str) -> list:
        """
        Get all residents for a specific planet
        
        Args:
            planet_id: The ID of the planet
            
        Returns:
            List of resident URLs
        """
        planet_data = self.get_planet(planet_id)
        return planet_data.get('residents', [])