#!/usr/bin/env python3

"""
OMDB API wrapper for fetching movie information.
Handles API communication and error cases.
"""

import requests
from typing import Optional, TypedDict
from dataclasses import dataclass
from datetime import datetime


class MovieInfo:
    """Container class for movie information."""
    def __init__(self, title: str, year: int, rating: float, poster_url: str, imdb_id: str, country: str):
        self.title = title
        self.year = year
        self.rating = rating
        self.poster_url = poster_url
        self.imdb_id = imdb_id
        self.country = country


class MovieAPI:
    """Class to interact with the OMDB API."""
    
    def __init__(self, api_key: str):
        """
        Initialize MovieAPI with API key.
        
        Args:
            api_key (str): OMDB API key
        """
        self._api_key = api_key
        self._base_url = "http://www.omdbapi.com/"
    
    def fetch_movie_info(self, title: str) -> Optional[MovieInfo]:
        """
        Fetch movie information from OMDB API.
        
        Args:
            title (str): Movie title to search for
            
        Returns:
            Optional[MovieInfo]: Movie information if found, None otherwise
        """
        try:
            params = {
                "apikey": self._api_key,
                "t": title,
                "plot": "short"
            }
            
            response = requests.get(self._base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("Response") == "False":
                print(f"Movie not found: {title}")
                return None
                
            # Extract and validate required fields
            title = data.get("Title")
            if not title:
                print(f"No title found for: {title}")
                return None
                
            try:
                year = int(data.get("Year", "0"))
                if year < 1888 or year > datetime.now().year:
                    print(f"Invalid year for: {title}")
                    return None
            except ValueError:
                print(f"Invalid year format for: {title}")
                return None
                
            try:
                rating = float(data.get("imdbRating", "0"))
                if rating < 0 or rating > 10:
                    print(f"Invalid rating for: {title}")
                    return None
            except ValueError:
                print(f"Invalid rating format for: {title}")
                return None
                
            # Extract country from the response
            country = data.get("Country", "")
            if country and "," in country:
                country = country.split(",")[0].strip()  # Take first country if multiple
                
            # Get poster URL
            poster_url = data.get("Poster", "")
            if poster_url == "N/A":
                poster_url = ""
                
            # Get IMDB ID
            imdb_id = data.get("imdbID", "")
                
            return MovieInfo(
                title=title,
                year=year,
                rating=rating,
                poster_url=poster_url,
                imdb_id=imdb_id,
                country=country
            )
            
        except requests.RequestException as e:
            print(f"API request error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None 