import os

def create_structure(base_path):
    # Define the folder structure
    folders = [
        "config",
        "core",
        "resources",
        "tests",
        "utils",
        "data/test_data",
        "data/results",
        "logs",
    ]
    
    # Define the files to be created
    files = {
        "config/__init__.py": "",
        "config/test_config.py": "# Configuration settings\n",
        "core/__init__.py": "",
        "core/api_client.py": "# Base API client\n",
        "core/logger.py": "# Logging configuration\n",
        "resources/__init__.py": "",
        "resources/people_api.py": "# People resource object\n",
        "resources/films_api.py": "# Films resource object\n",
        "resources/planets_api.py": "# Planets resource object\n",
        "resources/species_api.py": "# Species resource object\n",
        "tests/__init__.py": "",
        "tests/conftest.py": "# pytest configurations\n",
        "tests/test_cross_reference.py": "# Cross-reference tests\n",
        "tests/test_custom.py": "# Custom tests\n",
        "utils/__init__.py": "",
        "utils/data_handler.py": "# Test data handling utilities\n",
        "data/test_data/test_cases.csv": "# Test input data\n",
        "data/results/test_results.csv": "# Test results\n",
        "logs/swapi_tests.log": "",
        "requirements.txt": "# Project dependencies\n",
        "README.md": "# Project documentation\n",
    }
    
    # Create directories
    for folder in folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)
    
    # Create files with placeholders
    for file, content in files.items():
        file_path = os.path.join(base_path, file)
        with open(file_path, "w") as f:
            f.write(content)

# Usage
base_directory = "star_wars_api_testing"
create_structure(base_directory)
print(f"Directory structure created under '{base_directory}'")
