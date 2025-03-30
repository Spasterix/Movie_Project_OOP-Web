#!/usr/bin/env python3

"""
Configuration file for the movie management system.
Contains all necessary constants and settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Storage file paths
DEFAULT_JSON_FILE = "data/movies.json"
DEFAULT_CSV_FILE = "data/movies.csv"
TEST_JSON_FILE = "tests/test_movies.json"
TEST_CSV_FILE = "tests/test_movies.csv"

# OMDB API settings
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

# Website settings
WEBSITE_TITLE = os.getenv('WEBSITE_TITLE', 'My Movie Collection')
WEBSITE_OUTPUT = os.getenv('WEBSITE_OUTPUT', 'index.html') 