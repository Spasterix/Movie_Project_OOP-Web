#!/usr/bin/env python3

"""
Test module for the movie system.
Tests the core functionality of the movie application.
"""

import unittest
import os
import json
from src.movie_app import MovieApp
from src.storage.implementations.json_storage import StorageJson
from src.storage.implementations.csv_storage import StorageCsv
from src.movie_api import MovieAPI
from src.main import determine_storage
from src.config.config import (
    DEFAULT_JSON_FILE,
    DEFAULT_CSV_FILE,
    TEST_JSON_FILE,
    TEST_CSV_FILE
)


class TestMovieSystem(unittest.TestCase):
    """Testklasse für das Movie-Management-System."""
    
    def setUp(self):
        """Testumgebung vorbereiten."""
        self.test_json_file = "test_movies.json"
        self.test_csv_file = "test_movies.csv"
        
        # Stelle sicher, dass keine Test-Dateien existieren
        for file in [self.test_json_file, self.test_csv_file]:
            if os.path.exists(file):
                os.remove(file)
    
    def tearDown(self):
        """Testumgebung aufräumen."""
        # Entferne Test-Dateien
        for file in [self.test_json_file, self.test_csv_file]:
            if os.path.exists(file):
                os.remove(file)
    
    def test_json_storage(self):
        """Test der JSON Storage-Implementation."""
        storage = StorageJson(self.test_json_file)
        
        # Test: Leere Datenbank
        self.assertEqual(len(storage.list_movies()), 0)
        
        # Test: Film hinzufügen
        self.assertTrue(
            storage.add_movie(
                "Test Movie",
                2023,
                9.0,
                "http://example.com/poster.jpg",
                "Test notes",
                "tt1234567"
            )
        )
        
        # Test: Filme auflisten
        movies = storage.list_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies["Test Movie"]["year"], 2023)
        self.assertEqual(movies["Test Movie"]["rating"], 9.0)
        self.assertEqual(movies["Test Movie"]["poster_url"], "http://example.com/poster.jpg")
        self.assertEqual(movies["Test Movie"]["notes"], "Test notes")
        self.assertEqual(movies["Test Movie"]["imdb_id"], "tt1234567")
        
        # Test: Film aktualisieren
        self.assertTrue(
            storage.update_movie(
                "Test Movie",
                2024,
                9.5,
                "http://example.com/new_poster.jpg",
                "Updated notes",
                "tt7654321"
            )
        )
        
        # Test: Aktualisierung überprüfen
        movies = storage.list_movies()
        self.assertEqual(movies["Test Movie"]["year"], 2024)
        self.assertEqual(movies["Test Movie"]["rating"], 9.5)
        self.assertEqual(movies["Test Movie"]["poster_url"], "http://example.com/new_poster.jpg")
        self.assertEqual(movies["Test Movie"]["notes"], "Updated notes")
        self.assertEqual(movies["Test Movie"]["imdb_id"], "tt7654321")
        
        # Test: Film löschen
        self.assertTrue(storage.delete_movie("Test Movie"))
        self.assertEqual(len(storage.list_movies()), 0)
    
    def test_csv_storage(self):
        """Test der CSV Storage-Implementation."""
        storage = StorageCsv(self.test_csv_file)
        
        # Test: Leere Datenbank
        self.assertEqual(len(storage.list_movies()), 0)
        
        # Test: Film hinzufügen
        self.assertTrue(
            storage.add_movie(
                "Test Movie",
                2023,
                9.0,
                "http://example.com/poster.jpg",
                "Test notes",
                "tt1234567"
            )
        )
        
        # Test: Filme auflisten
        movies = storage.list_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies["Test Movie"]["year"], 2023)
        self.assertEqual(movies["Test Movie"]["rating"], 9.0)
        self.assertEqual(movies["Test Movie"]["poster_url"], "http://example.com/poster.jpg")
        self.assertEqual(movies["Test Movie"]["notes"], "Test notes")
        self.assertEqual(movies["Test Movie"]["imdb_id"], "tt1234567")
        
        # Test: Film aktualisieren
        self.assertTrue(
            storage.update_movie(
                "Test Movie",
                2024,
                9.5,
                "http://example.com/new_poster.jpg",
                "Updated notes",
                "tt7654321"
            )
        )
        
        # Test: Aktualisierung überprüfen
        movies = storage.list_movies()
        self.assertEqual(movies["Test Movie"]["year"], 2024)
        self.assertEqual(movies["Test Movie"]["rating"], 9.5)
        self.assertEqual(movies["Test Movie"]["poster_url"], "http://example.com/new_poster.jpg")
        self.assertEqual(movies["Test Movie"]["notes"], "Updated notes")
        self.assertEqual(movies["Test Movie"]["imdb_id"], "tt7654321")
        
        # Test: Film löschen
        self.assertTrue(storage.delete_movie("Test Movie"))
        self.assertEqual(len(storage.list_movies()), 0)
    
    def test_movie_api(self):
        """Test der OMDB API Integration."""
        api = MovieAPI("348067e7")
        
        # Test: Existierenden Film abrufen
        movie_info = api.fetch_movie_info("The Shawshank Redemption")
        self.assertIsNotNone(movie_info)
        self.assertEqual(movie_info.title, "The Shawshank Redemption")
        self.assertEqual(movie_info.year, 1994)
        self.assertGreater(movie_info.rating, 0)
        self.assertIsNotNone(movie_info.imdb_id)
        
        # Test: Nicht existierenden Film abrufen
        movie_info = api.fetch_movie_info("This Movie Does Not Exist 123")
        self.assertIsNone(movie_info)
    
    def test_movie_app(self):
        """Test der MovieApp Hauptklasse."""
        app = MovieApp(storage_type="json", storage_path=self.test_json_file)
        self.assertIsInstance(app._storage, StorageJson)
        app._command_generate_website()
    
    def test_storage_detection(self):
        """Test der Storage-Typ-Erkennung."""
        # Test: JSON Storage
        app = MovieApp(storage_type="json", storage_path=self.test_json_file)
        self.assertIsInstance(app._storage, StorageJson)
        
        # Test: CSV Storage
        app = MovieApp(storage_type="csv", storage_path=self.test_csv_file)
        self.assertIsInstance(app._storage, StorageCsv)


def main():
    """Hauptfunktion zum Ausführen der Tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    main() 