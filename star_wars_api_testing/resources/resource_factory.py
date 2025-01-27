from typing import Dict, Any
from .films_api import FilmsAPI
from .people_api import PeopleAPI
from .planets_api import PlanetsAPI
from .species_api import SpeciesAPI


class ResourceFactory:
    def __init__(self, client):
        self.client = client
        self._resources: Dict[str, Any] = {}
    
    @property
    def films(self) -> FilmsAPI:
        if 'films' not in self._resources:
            self._resources['films'] = FilmsAPI(self.client)
        return self._resources['films']
    
    @property
    def people(self) -> PeopleAPI:
        if 'people' not in self._resources:
            self._resources['people'] = PeopleAPI(self.client)
        return self._resources['people']
    
    @property
    def planets(self) -> PlanetsAPI:
        if 'planets' not in self._resources:
            self._resources['planets'] = PlanetsAPI(self.client)
        return self._resources['planets']
    
    @property
    def species(self) -> SpeciesAPI:
        if 'species' not in self._resources:
            self._resources['species'] = SpeciesAPI(self.client)
        return self._resources['species']
    
