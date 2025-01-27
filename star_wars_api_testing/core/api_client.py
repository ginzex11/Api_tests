# Base API client
# core/api_client.py
import requests
import logging
from typing import Dict, Any
from config.test_config import TestConfig

class SwapiClient:
    def __init__(self, base_url: str = TestConfig.BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"Making GET request to: {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise