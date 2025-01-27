# Configuration settings
# config/test_config.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TestConfig:
    BASE_URL: str = "https://swapi.py4e.com/api"
    ROOT_DIR: Path = Path(__file__).parent.parent
    LOG_DIR: Path = ROOT_DIR / "logs"
    DATA_DIR: Path = ROOT_DIR / "data"  
    TEST_DATA_FILE: Path = DATA_DIR / "test_data" / "test_cases.csv"
    RESULTS_FILE: Path = DATA_DIR / "results" / "test_results.csv"
    LOG_FILE: Path = LOG_DIR / "swapi_tests.log"