"""
Konfigurationsdatei für das Movie Management System.
Enthält wichtige Konstanten und Einstellungen.
"""

# OMDB API Konfiguration
OMDB_API_KEY = "348067e7"

# Dateipfade
DEFAULT_JSON_FILE = "data/movies.json"
DEFAULT_CSV_FILE = "data/movies.csv"
DEFAULT_HTML_TEMPLATE = "templates/movie_template.html"

# Website Einstellungen
WEBSITE_TITLE = "My Movie App"
WEBSITE_OUTPUT = "index.html"

# API Einstellungen
API_TIMEOUT = 10  # Sekunden
API_RETRIES = 3   # Anzahl der Wiederholungsversuche 