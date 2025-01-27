# core/api_client.py

import requests
import logging
import time
from typing import Dict, Any
from star_wars_api_testing.config.test_config import TestConfig

class SwapiClient:
    def __init__(self, base_url: str = TestConfig.BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"Making GET request to: {url}")

        start_time = time.time()

        try:
            response = self.session.get(url)
            response.raise_for_status()
            duration = time.time() - start_time
            self.logger.info(f"Request completed in {duration:.2f} seconds: {url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
