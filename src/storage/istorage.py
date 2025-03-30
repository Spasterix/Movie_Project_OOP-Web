#!/usr/bin/env python3

"""
Interface definition for movie storage implementations.
Provides a contract for different storage types (JSON, CSV, etc.).
"""

from abc import ABC, abstractmethod
from typing import Dict, TypedDict


class MovieData(TypedDict):
    """Type definition for movie data structure."""
    rating: float
    year: int
    poster_url: str
    country: str  # Country code (e.g., "US", "GB", "DE")
    notes: str  # Neue Feld für Notizen
    imdb_id: str  # IMDB ID für den direkten Link


class IStorage(ABC):
    """
    Abstract base class defining the interface for movie storage implementations.
    All storage classes (JSON, CSV, etc.) must implement these methods.
    """
    
    @abstractmethod
    def list_movies(self) -> Dict[str, MovieData]:
        """
        Returns a dictionary of all movies in the storage.
        
        Returns:
            Dict[str, MovieData]: Dictionary with movie titles as keys and movie data as values.
            Example:
            {
                "Movie Title": {
                    "rating": 7.5,
                    "year": 2021,
                    "poster_url": "http://...",
                    "notes": "My favorite movie!"
                }
            }
        """
        pass

    @abstractmethod
    def add_movie(self, title: str, year: int, rating: float, poster_url: str = "", notes: str = "") -> bool:
        """
        Adds a new movie to the storage.
        
        Args:
            title (str): The title of the movie
            year (int): The release year of the movie
            rating (float): The rating of the movie
            poster_url (str, optional): URL to movie poster image
            notes (str, optional): Personal notes about the movie
            
        Returns:
            bool: True if movie was added successfully, False if movie already exists
        """
        pass

    @abstractmethod
    def delete_movie(self, title: str) -> bool:
        """
        Deletes a movie from the storage.
        
        Args:
            title (str): The title of the movie to delete
            
        Returns:
            bool: True if movie was deleted successfully, False if movie was not found
        """
        pass

    @abstractmethod
    def update_movie(self, title: str, rating: float, year: int, notes: str = "") -> bool:
        """
        Updates the rating, year and notes of an existing movie.
        
        Args:
            title (str): The title of the movie to update
            rating (float): The new rating for the movie
            year (int): The new year for the movie
            notes (str, optional): New notes for the movie
            
        Returns:
            bool: True if movie was updated successfully, False if movie was not found
        """
        pass 