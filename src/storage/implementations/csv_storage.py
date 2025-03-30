#!/usr/bin/env python3

"""
CSV file-based implementation of the movie storage interface.
Handles persistence of movie data in CSV format.
"""

import csv
import os
from typing import Dict, List, Optional
from src.storage.istorage import IStorage, MovieData


class StorageCsv(IStorage):
    """CSV-basierte Implementierung des IStorage Interface."""
    
    def __init__(self, filename: str = "movies.csv"):
        """Initialisiere CSV Storage mit Dateinamen."""
        self._filename = filename
        self._storage: Dict[str, MovieData] = {}
        self._read_storage()
    
    def _read_storage(self) -> None:
        """Lese die CSV-Datei und konvertiere sie in das interne Speicherformat."""
        try:
            if os.path.exists(self._filename):
                with open(self._filename, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self._storage[row['title']] = {
                            'year': int(row['year']),
                            'rating': float(row['rating']),
                            'poster_url': row.get('poster_url') or None,
                            'notes': row.get('notes', ""),
                            'imdb_id': row.get('imdb_id') or None,
                            'country': row.get('country', "")
                        }
        except (csv.Error, IOError, ValueError) as e:
            print(f"Error reading storage: {str(e)}")
            self._storage = {}
    
    def _write_storage(self, storage: Dict[str, MovieData]) -> None:
        """Schreibe den aktuellen Speicherinhalt in die CSV-Datei."""
        try:
            fieldnames = ['title', 'year', 'rating', 'poster_url', 'notes', 'imdb_id', 'country']
            with open(self._filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for title, data in storage.items():
                    writer.writerow({
                        'title': title,
                        'year': data['year'],
                        'rating': data['rating'],
                        'poster_url': data.get('poster_url', ""),
                        'notes': data.get('notes', ""),
                        'imdb_id': data.get('imdb_id', ""),
                        'country': data.get('country', "")
                    })
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
        if title in self._storage:
            return False
            
        self._storage[title] = {
            'year': year,
            'rating': rating,
            'poster_url': poster_url,
            'notes': notes,
            'imdb_id': imdb_id,
            'country': country
        }
        self._write_storage(self._storage)
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
        if title not in self._storage:
            return False
            
        self._storage[title] = {
            'year': year,
            'rating': rating,
            'poster_url': poster_url,
            'notes': notes,
            'imdb_id': imdb_id,
            'country': country
        }
        self._write_storage(self._storage)
        return True
    
    def delete_movie(self, title: str) -> bool:
        """Lösche einen Film aus dem Speicher."""
        if title not in self._storage:
            return False
            
        del self._storage[title]
        self._write_storage(self._storage)
        return True
    
    def list_movies(self) -> Dict[str, MovieData]:
        """Liste alle Filme im Speicher auf."""
        return self._storage.copy() 