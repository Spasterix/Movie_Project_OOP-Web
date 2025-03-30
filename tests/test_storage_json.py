#!/usr/bin/env python3

"""
Test suite for JSON storage implementation.
"""

import unittest
import os
import json
from src.storage.implementations.json_storage import StorageJson


def main():
    """Run practical tests for StorageJson class."""
    # Test file path
    test_file = "test_movies.json"
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create storage instance
    print("Creating storage instance...")
    storage = StorageJson(test_file)
    
    # Test adding movies
    print("\nTesting add_movie()...")
    print(f"Adding 'Test Movie 1': {storage.add_movie('Test Movie 1', 2020, 8.5)}")
    print(f"Adding 'Test Movie 2': {storage.add_movie('Test Movie 2', 2021, 7.5)}")
    print(f"Adding duplicate movie: {storage.add_movie('Test Movie 1', 2020, 8.5)}")
    
    # Test listing movies
    print("\nTesting list_movies()...")
    movies = storage.list_movies()
    print("Current movies in storage:")
    for title, data in movies.items():
        print(f"- {title}: Year={data['year']}, Rating={data['rating']}")
    
    # Test updating movie
    print("\nTesting update_movie()...")
    print(f"Updating 'Test Movie 1': {storage.update_movie('Test Movie 1', 9.0, 2020)}")
    print(f"Updating non-existent movie: {storage.update_movie('Non Existent', 5.0, 2000)}")
    
    # Test deleting movie
    print("\nTesting delete_movie()...")
    print(f"Deleting 'Test Movie 2': {storage.delete_movie('Test Movie 2')}")
    print(f"Deleting non-existent movie: {storage.delete_movie('Non Existent')}")
    
    # Show final state
    print("\nFinal state of storage:")
    movies = storage.list_movies()
    for title, data in movies.items():
        print(f"- {title}: Year={data['year']}, Rating={data['rating']}")
    
    # Clean up test file
    os.remove(test_file)
    print("\nTest completed and test file cleaned up.")


if __name__ == "__main__":
    main() 