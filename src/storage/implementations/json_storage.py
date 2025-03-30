#!/usr/bin/env python3

"""
JSON file-based implementation of the movie storage interface.
Handles persistence of movie data in JSON format.
"""

import json
import os
from typing import Dict, Optional
from src.storage.istorage import IStorage, MovieData


class StorageJson(IStorage):
    """JSON file-based implementation of the movie storage interface."""
    
    def __init__(self, filename: str = "movies.json"):
        """Initialize JSON storage with filename."""
        self._filename = filename
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self) -> None:
        """Ensure storage file exists with initial empty structure."""
        if not os.path.exists(self._filename):
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def _read_storage(self) -> Dict[str, MovieData]:
        """
        Read the current state from storage file.
        
        Returns:
            Dict[str, MovieData]: Current movies data
        """
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure all movies have required fields
                for movie_data in data.values():
                    if 'poster_url' not in movie_data:
                        movie_data['poster_url'] = ""
                    if 'notes' not in movie_data:
                        movie_data['notes'] = ""
                    if 'imdb_id' not in movie_data:
                        movie_data['imdb_id'] = ""
                    if 'country' not in movie_data:
                        movie_data['country'] = ""
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading storage: {str(e)}")
            return {}
    
    def _write_storage(self, movies: Dict[str, MovieData]) -> None:
        """
        Write movies data to storage file.
        
        Args:
            movies (Dict[str, MovieData]): Movies data to write
        """
        try:
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump(movies, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error writing storage: {str(e)}")
    
    def add_movie(self, title: str, year: int, rating: float, poster_url: str = "", notes: str = "", imdb_id: str = "", country: str = "") -> bool:
        """
        Adds a new movie to the storage.
        
        Args:
            title (str): The title of the movie
            year (int): The release year of the movie
            rating (float): The rating of the movie
            poster_url (str, optional): URL to movie poster image
            notes (str, optional): Notes about the movie
            imdb_id (str, optional): IMDB ID for direct linking
            country (str, optional): Country of origin
            
        Returns:
            bool: True if movie was added successfully, False if movie already exists
        """
        movies = self._read_storage()
        if title in movies:
            return False
            
        movies[title] = {
            "rating": rating,
            "year": year,
            "poster_url": poster_url,
            "notes": notes,
            "imdb_id": imdb_id,
            "country": country
        }
        self._write_storage(movies)
        return True
    
    def update_movie(self, title: str, year: int, rating: float, poster_url: str = "", notes: str = "", imdb_id: str = "", country: str = "") -> bool:
        """
        Updates an existing movie in the storage.
        
        Args:
            title (str): The title of the movie to update
            year (int): The new year for the movie
            rating (float): The new rating for the movie
            poster_url (str, optional): New poster URL for the movie
            notes (str, optional): New notes for the movie
            imdb_id (str, optional): New IMDB ID for the movie
            country (str, optional): New country for the movie
            
        Returns:
            bool: True if movie was updated successfully, False if movie was not found
        """
        movies = self._read_storage()
        if title not in movies:
            return False
            
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster_url": poster_url,
            "notes": notes,
            "imdb_id": imdb_id,
            "country": country
        }
        self._write_storage(movies)
        return True
    
    def delete_movie(self, title: str) -> bool:
        """Delete a movie from storage."""
        movies = self._read_storage()
        if title not in movies:
            return False
            
        del movies[title]
        self._write_storage(movies)
        return True
    
    def list_movies(self) -> Dict[str, MovieData]:
        """List all movies in storage."""
        return self._read_storage() 