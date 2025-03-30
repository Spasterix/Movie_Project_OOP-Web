#!/usr/bin/env python3

"""
Test suite for storage interface.
"""

import unittest
from src.storage.istorage import IStorage, MovieData


def main():
    """
    Simple verification that our interface is correctly defined.
    This will raise a TypeError if we try to instantiate the abstract class.
    """
    try:
        # This should fail as we cannot instantiate an abstract class
        storage = IStorage()  # type: ignore
        print("Test failed: Should not be able to instantiate IStorage directly!")
    except TypeError as e:
        print("Test passed: Cannot instantiate abstract class IStorage")
        print(f"Error message: {str(e)}")
        
    # Print the expected method signatures for implementation
    print("\nRequired methods to implement:")
    print("--------------------------------")
    print("list_movies() -> Dict[str, MovieData]")
    print("add_movie(title: str, year: int, rating: float) -> bool")
    print("delete_movie(title: str) -> bool")
    print("update_movie(title: str, rating: float, year: int) -> bool")
    
    # Print the expected MovieData structure
    print("\nMovieData structure:")
    print("--------------------------------")
    print("MovieData:")
    print("  - rating: float")
    print("  - year: int")


if __name__ == "__main__":
    main() 