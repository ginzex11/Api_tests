# star_wars_api_testing/tests/conftest.py
import pytest
import os
import sys

# Add  project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)