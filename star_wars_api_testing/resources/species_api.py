# Species resource object
from typing import Dict, Any, List
import logging

class SpeciesAPI:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def get_species(self, species_id: str) -> Dict[str, Any]:
        """
        Get details for a specific species
        
        Args:
            species_id: The ID of the species to retrieve
            
        Returns:
            Dict containing species details
        """
        self.logger.info(f"Fetching species with ID: {species_id}")
        return self.client.get(f"species/{species_id}")
    
    def get_people(self, species_id: str) -> List[str]:
        """Get all people of this species"""
        species_data = self.get_species(species_id)
        return species_data.get('people', [])
    
    def get_films(self, species_id: str) -> List[str]:
        """Get all films featuring this species"""
        species_data = self.get_species(species_id)
        return species_data.get('films', [])
    
    def get_homeworld(self, species_id: str) -> str:
        """Get species homeworld"""
        species_data = self.get_species(species_id)
        return species_data.get('homeworld', '')