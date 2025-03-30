#!/usr/bin/env python3

"""
Movie application class that handles the user interface and business logic.
Uses a storage implementation to persist movie data.
"""

import os
import random
import statistics
from typing import Dict, Optional
from src.storage.istorage import IStorage, MovieData
from src.movie_api import MovieAPI
from src.storage.implementations.json_storage import StorageJson
from src.storage.implementations.csv_storage import StorageCsv
from config.config import (
    OMDB_API_KEY,
    WEBSITE_TITLE,
    WEBSITE_OUTPUT
)


class MovieApp:
    """Main movie application class that handles user interaction and movie operations."""

    def __init__(self, storage_type: str = "json", storage_path: str = "movies.json"):
        """
        Initialize MovieApp with a storage implementation.
        
        Args:
            storage_type (str): Type of storage ("json" or "csv")
            storage_path (str): Path to storage file
        """
        self._api = MovieAPI("348067e7")
        
        if storage_type == "json":
            self._storage = StorageJson(storage_path)
        elif storage_type == "csv":
            self._storage = StorageCsv(storage_path)
        else:
            raise ValueError(f"Invalid storage type: {storage_type}")
            
        self._commands = {
            "1": ("List Movies", self._command_list_movies),
            "2": ("Add Movie", self._command_add_movie),
            "3": ("Delete Movie", self._command_delete_movie),
            "4": ("Update Movie", self._command_update_movie),
            "5": ("Stats", self._command_movie_stats),
            "6": ("Random Movie", self._command_random_movie),
            "7": ("Search Movie", self._command_search_movie),
            "8": ("Movies Sorted by Rating", self._command_sort_by_rating),
            "9": ("Movies Sorted by Year", self._command_sort_by_year),
            "10": ("Generate Website", self._command_generate_website),
            "0": ("Exit", self._command_exit)
        }

    def _clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_menu(self) -> None:
        """Display the main menu options."""
        self._clear_screen()
        print("\n=== Movie Database Menu ===")
        for key, (name, _) in self._commands.items():
            print(f"{key}. {name}")
        print("=" * 25)

    def _get_valid_rating(self) -> float:
        """
        Get valid rating input from user.
        
        Returns:
            float: Valid rating between 1 and 10
        """
        while True:
            try:
                rating = float(input("Enter movie rating (1-10): "))
                if 1 <= rating <= 10:
                    return rating
                print("Error: Rating must be between 1 and 10")
            except ValueError:
                print("Error: Invalid rating format")

    def _get_valid_year(self) -> int:
        """
        Get valid year input from user.
        
        Returns:
            int: Valid year between 1888 and current year
        """
        from datetime import datetime
        current_year = datetime.now().year
        
        while True:
            try:
                year = int(input(f"Enter movie year (1888-{current_year}): "))
                if 1888 <= year <= current_year:
                    return year
                print(f"Error: Year must be between 1888 and {current_year}")
            except ValueError:
                print("Error: Invalid year format")

    def _command_list_movies(self) -> None:
        """Display all movies in the database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in database.")
            return
            
        print(f"\n{len(movies)} movies in total:")
        for title, data in movies.items():
            print(f"{title} ({data['year']}): {data['rating']:.1f}")

    def _command_add_movie(self) -> None:
        """Add a new movie to the database using OMDB API."""
        title = input("Enter movie title: ").strip()
        if not title:
            print("Error: Title cannot be empty")
            return
            
        try:
            # Fetch movie info from API
            movie_info = self._api.fetch_movie_info(title)
            
            if movie_info is None:
                print(f"Error: Movie '{title}' not found in OMDB database")
                return
                
            # Add movie to storage
            if self._storage.add_movie(
                movie_info.title,
                movie_info.year,
                movie_info.rating,
                movie_info.poster_url,
                "",  # Empty note
                movie_info.imdb_id,
                movie_info.country  # Add country
            ):
                print(f"Movie '{movie_info.title}' added successfully")
                print(f"Year: {movie_info.year}")
                print(f"Rating: {movie_info.rating}")
                print(f"Country: {movie_info.country}")
                if movie_info.poster_url:
                    print(f"Poster URL: {movie_info.poster_url}")
                print(f"IMDB: https://www.imdb.com/title/{movie_info.imdb_id}/")
            else:
                print(f"Error: Movie '{movie_info.title}' already exists")
                
        except ConnectionError:
            print("Error: No internet connection available")
            print("Tip: Check your internet connection and try again")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Tip: Try again later")

    def _command_delete_movie(self) -> None:
        """Delete a movie from the database."""
        title = input("Enter movie title to delete: ").strip()
        if not title:
            print("Error: Title cannot be empty")
            return
            
        if self._storage.delete_movie(title):
            print(f"Movie '{title}' deleted successfully")
        else:
            print(f"Error: Movie '{title}' not found")

    def _command_update_movie(self) -> None:
        """Update an existing movie's notes."""
        title = input("Enter movie name: ").strip()
        if not title:
            print("Error: Title cannot be empty")
            return
            
        movies = self._storage.list_movies()
        if title not in movies:
            print(f"Error: Movie '{title}' not found")
            return
            
        notes = input("Enter movie notes: ").strip()
        movie = movies[title]
        
        if self._storage.update_movie(
            title,
            movie['rating'],
            movie['year'],
            notes
        ):
            print(f"Movie '{title}' successfully updated")
        else:
            print(f"Error updating movie '{title}'")

    def _command_movie_stats(self) -> None:
        """Display movie statistics."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in database")
            return

        ratings = [data['rating'] for data in movies.values()]
        avg_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        best_rating = max(ratings)
        worst_rating = min(ratings)

        print("\nMovie Statistics:")
        print(f"Average rating: {avg_rating:.1f}")
        print(f"Median rating: {median_rating:.1f}")
        
        print("\nBest rated movies:")
        for title, data in movies.items():
            if data['rating'] == best_rating:
                print(f"{title}: {data['rating']:.1f}")
                
        print("\nWorst rated movies:")
        for title, data in movies.items():
            if data['rating'] == worst_rating:
                print(f"{title}: {data['rating']:.1f}")

    def _command_random_movie(self) -> None:
        """Display a random movie from the database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in database")
            return
            
        title = random.choice(list(movies.keys()))
        data = movies[title]
        print(f"\nYour random movie is:")
        print(f"{title} ({data['year']}): {data['rating']:.1f}")
        if data.get('poster_url'):
            print(f"Poster: {data['poster_url']}")

    def _command_search_movie(self) -> None:
        """Search for movies by title."""
        search_term = input("Enter search term: ").strip().lower()
        if not search_term:
            print("Error: Search term cannot be empty")
            return
            
        movies = self._storage.list_movies()
        found = False
        
        print("\nSearch results:")
        for title, data in movies.items():
            if search_term in title.lower():
                print(f"{title} ({data['year']}): {data['rating']:.1f}")
                if data.get('poster_url'):
                    print(f"Poster: {data['poster_url']}")
                found = True
                
        if not found:
            print("No movies found matching your search")

    def _command_sort_by_rating(self) -> None:
        """Display movies sorted by rating."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in database")
            return
            
        sorted_movies = sorted(
            movies.items(),
            key=lambda x: (x[1]['rating'], x[0]),
            reverse=True
        )
        
        print("\nMovies sorted by rating (highest to lowest):")
        for title, data in sorted_movies:
            print(f"{title} ({data['year']}): {data['rating']:.1f}")

    def _command_sort_by_year(self) -> None:
        """Display movies sorted by year."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in database")
            return
            
        order = input("Sort by (n)ewest or (o)ldest first? ").lower()
        if order not in ['n', 'o']:
            print("Invalid choice")
            return
            
        sorted_movies = sorted(
            movies.items(),
            key=lambda x: x[1]['year'],
            reverse=(order == 'n')
        )
        
        print(f"\nMovies sorted by year ({'newest' if order == 'n' else 'oldest'} first):")
        for title, data in sorted_movies:
            print(f"{title} ({data['year']}): {data['rating']:.1f}")

    def _command_generate_website(self) -> None:
        """Generate an HTML website displaying the movie database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to display")
            return
            
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Movie Collection</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #34495e;
            --accent-color: #3498db;
            --text-color: #2c3e50;
            --background-color: #ecf0f1;
            --card-background: #ffffff;
            --hover-color: rgba(52, 152, 219, 0.1);
        }
        
        body { 
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            padding: 0;
            margin: 0;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
            text-align: center;
        }
        
        .header p {
            margin: 0.5rem 0 0;
            text-align: center;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .movie-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 1rem;
        }
        
        .movie-card {
            background: var(--card-background);
            border-radius: 10px;
            box-shadow: 0 3px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        .movie-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        .movie-poster-container {
            position: relative;
            padding-top: 150%;
            overflow: hidden;
            background: var(--secondary-color);
        }
        
        .movie-poster {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .movie-card:hover .movie-poster {
            transform: scale(1.05);
        }
        
        .movie-info {
            padding: 1.2rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .movie-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0 0 0.5rem;
            color: var(--text-color);
            line-height: 1.3;
        }
        
        .movie-year {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .country-flag {
            font-size: 1.2rem;
            margin-left: 0.5rem;
        }
        
        .movie-rating {
            margin: 0.5rem 0;
        }
        
        .star-filled {
            color: #f1c40f;
        }
        
        .star-empty {
            color: #bdc3c7;
        }
        
        .rating-number {
            color: #666;
            font-size: 0.9rem;
            margin-left: 0.5rem;
            vertical-align: middle;
        }
        
        .imdb-link {
            position: absolute;
            top: 0.8rem;
            right: 0.8rem;
            background: rgba(0,0,0,0.7);
            color: #f3ce13;
            padding: 0.4rem 0.8rem;
            border-radius: 5px;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 2;
        }
        
        .movie-card:hover .imdb-link {
            opacity: 1;
        }
        
        .imdb-link:hover {
            background: rgba(0,0,0,0.8);
            color: #f3ce13;
            text-decoration: none;
        }
        
        .watch-link {
            position: absolute;
            top: 0.8rem;
            right: 7rem;
            background: rgba(0,0,0,0.7);
            color: #2ecc71;
            padding: 0.4rem 0.8rem;
            border-radius: 5px;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 2;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }
        
        .watch-link i {
            font-size: 1rem;
        }
        
        .movie-card:hover .watch-link {
            opacity: 1;
        }
        
        .watch-link:hover {
            background: rgba(0,0,0,0.8);
            color: #2ecc71;
            text-decoration: none;
        }
        
        .movie-notes {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(44, 62, 80, 0.95);
            color: white;
            padding: 2rem;
            opacity: 0;
            transition: opacity 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            z-index: 1;
        }
        
        .movie-card:hover .movie-notes {
            opacity: 1;
        }
        
        .movie-notes p {
            margin: 0;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        .pagination {
            display: flex;
            justify-content: center;
            margin: 2rem 0;
            gap: 0.5rem;
        }
        
        .page-button {
            background: var(--card-background);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .page-button:hover {
            background: var(--hover-color);
        }
        
        .page-button.active {
            background: var(--accent-color);
            color: white;
        }
        
        @media (max-width: 768px) {
            .movie-grid {
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .movie-title {
                font-size: 1rem;
            }
        }
        
        @media (max-width: 480px) {
            .movie-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 0.8rem;
            }
            
            .movie-info {
                padding: 0.8rem;
            }
            
            .header h1 {
                font-size: 1.5rem;
            }
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const ITEMS_PER_PAGE = 12;
            const movieCards = document.querySelectorAll('.movie-card');
            const totalPages = Math.ceil(movieCards.length / ITEMS_PER_PAGE);
            let currentPage = 1;
            
            function showPage(page) {
                const start = (page - 1) * ITEMS_PER_PAGE;
                const end = start + ITEMS_PER_PAGE;
                
                movieCards.forEach((card, index) => {
                    card.style.display = (index >= start && index < end) ? 'flex' : 'none';
                });
                
                // Update active button
                document.querySelectorAll('.page-button').forEach(button => {
                    button.classList.toggle('active', parseInt(button.dataset.page) === page);
                });
                
                // Scroll to top smoothly
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            
            // Create pagination
            if (totalPages > 1) {
                const pagination = document.createElement('div');
                pagination.className = 'pagination';
                
                for (let i = 1; i <= totalPages; i++) {
                    const button = document.createElement('button');
                    button.className = 'page-button';
                    button.textContent = i;
                    button.dataset.page = i;
                    button.onclick = () => {
                        currentPage = i;
                        showPage(i);
                    };
                    pagination.appendChild(button);
                }
                
                document.querySelector('.container').appendChild(pagination);
            }
            
            // Show first page initially
            showPage(1);
        });
    </script>
</head>
<body>
    <header class="header">
        <h1>My Movie Collection</h1>
        <p>A collection of my favorite movies</p>
    </header>
    
    <div class="container">
        <div class="movie-grid">
"""
        
        def generate_star_rating(rating: float) -> str:
            """Generate HTML for star rating display."""
            rating_5 = rating / 2
            filled_stars = int(rating_5)
            half_star = rating_5 - filled_stars >= 0.5
            empty_stars = 5 - filled_stars - (1 if half_star else 0)
            
            stars_html = (
                '<i class="bi bi-star-fill star-filled"></i>' * filled_stars +
                ('<i class="bi bi-star-half star-filled"></i>' if half_star else '') +
                '<i class="bi bi-star star-empty"></i>' * empty_stars
            )
            
            return f"""
            <div class="movie-rating">
                {stars_html}
                <span class="rating-number">({rating:.1f}/10)</span>
            </div>"""
        
        def get_country_code(country_name: str) -> str:
            """
            Convert country name to ISO country code.
            
            Args:
                country_name (str): Full country name (e.g., "United States", "United Kingdom")
                
            Returns:
                str: Two-letter ISO country code (e.g., "US", "GB")
            """
            # Dictionary mapping country names to ISO codes
            country_codes = {
                "United States": "US",
                "United Kingdom": "GB",
                "Germany": "DE",
                "New Zealand": "NZ",
                "France": "FR",
                "Italy": "IT",
                "Spain": "ES",
                "Japan": "JP",
                "China": "CN",
                "India": "IN",
                "Australia": "AU",
                "Canada": "CA",
                "Brazil": "BR",
                "Russia": "RU",
                "South Korea": "KR",
                "Mexico": "MX",
                "Sweden": "SE",
                "Norway": "NO",
                "Denmark": "DK",
                "Finland": "FI",
                "Netherlands": "NL",
                "Belgium": "BE",
                "Austria": "AT",
                "Switzerland": "CH",
                "Poland": "PL",
                "Czech Republic": "CZ",
                "Hungary": "HU",
                "Romania": "RO",
                "Bulgaria": "BG",
                "Greece": "GR",
                "Turkey": "TR",
                "Israel": "IL",
                "South Africa": "ZA",
                "Egypt": "EG",
                "Nigeria": "NG",
                "Argentina": "AR",
                "Chile": "CL",
                "Colombia": "CO",
                "Venezuela": "VE",
                "Peru": "PE",
                "Thailand": "TH",
                "Vietnam": "VN",
                "Malaysia": "MY",
                "Singapore": "SG",
                "Philippines": "PH",
                "Indonesia": "ID",
                "Pakistan": "PK",
                "Bangladesh": "BD",
                "Sri Lanka": "LK",
                "Nepal": "NP",
                "Afghanistan": "AF",
                "Iran": "IR",
                "Iraq": "IQ",
                "Saudi Arabia": "SA",
                "United Arab Emirates": "AE",
                "Kuwait": "KW",
                "Qatar": "QA",
                "Bahrain": "BH",
                "Oman": "OM",
                "Yemen": "YE",
                "Syria": "SY",
                "Lebanon": "LB",
                "Jordan": "JO",
                "Palestine": "PS",
                "Cyprus": "CY",
                "Malta": "MT",
                "Iceland": "IS",
                "Ireland": "IE",
                "Portugal": "PT",
                "Luxembourg": "LU",
                "Slovakia": "SK",
                "Slovenia": "SI",
                "Croatia": "HR",
                "Serbia": "RS",
                "Montenegro": "ME",
                "Albania": "AL",
                "Macedonia": "MK",
                "Bosnia and Herzegovina": "BA",
                "Kosovo": "XK",
                "Moldova": "MD",
                "Ukraine": "UA",
                "Belarus": "BY",
                "Estonia": "EE",
                "Latvia": "LV",
                "Lithuania": "LT",
                "Georgia": "GE",
                "Armenia": "AM",
                "Azerbaijan": "AZ",
                "Kazakhstan": "KZ",
                "Uzbekistan": "UZ",
                "Turkmenistan": "TM",
                "Kyrgyzstan": "KG",
                "Tajikistan": "TJ",
                "Mongolia": "MN",
                "North Korea": "KP",
                "Taiwan": "TW",
                "Hong Kong": "HK",
                "Macau": "MO",
                "Cambodia": "KH",
                "Laos": "LA",
                "Myanmar": "MM",
                "Brunei": "BN",
                "East Timor": "TL",
                "Fiji": "FJ",
                "Samoa": "WS",
                "Tonga": "TO",
                "Vanuatu": "VU",
                "Solomon Islands": "SB",
                "Papua New Guinea": "PG",
                "New Caledonia": "NC",
                "French Polynesia": "PF",
                "Guam": "GU",
                "Northern Mariana Islands": "MP",
                "American Samoa": "AS",
                "Puerto Rico": "PR",
                "Virgin Islands": "VI",
                "Bermuda": "BM",
                "Greenland": "GL",
                "Faroe Islands": "FO",
                "Åland Islands": "AX",
                "Gibraltar": "GI",
                "Andorra": "AD",
                "Liechtenstein": "LI",
                "Monaco": "MC",
                "San Marino": "SM",
                "Vatican City": "VA",
                "Cuba": "CU",
                "Haiti": "HT",
                "Dominican Republic": "DO",
                "Jamaica": "JM",
                "Trinidad and Tobago": "TT",
                "Bahamas": "BS",
                "Barbados": "BB",
                "Saint Lucia": "LC",
                "Saint Vincent and the Grenadines": "VC",
                "Grenada": "GD",
                "Antigua and Barbuda": "AG",
                "Saint Kitts and Nevis": "KN",
                "Dominica": "DM",
                "Suriname": "SR",
                "Guyana": "GY",
                "Paraguay": "PY",
                "Uruguay": "UY",
                "Ecuador": "EC",
                "Bolivia": "BO",
                "Panama": "PA",
                "Costa Rica": "CR",
                "Nicaragua": "NI",
                "Honduras": "HN",
                "El Salvador": "SV",
                "Guatemala": "GT",
                "Belize": "BZ",
                "Algeria": "DZ",
                "Angola": "AO",
                "Benin": "BJ",
                "Botswana": "BW",
                "Burkina Faso": "BF",
                "Burundi": "BI",
                "Cameroon": "CM",
                "Cape Verde": "CV",
                "Central African Republic": "CF",
                "Chad": "TD",
                "Comoros": "KM",
                "Congo": "CG",
                "Democratic Republic of the Congo": "CD",
                "Djibouti": "DJ",
                "Equatorial Guinea": "GQ",
                "Eritrea": "ER",
                "Ethiopia": "ET",
                "Gabon": "GA",
                "Gambia": "GM",
                "Ghana": "GH",
                "Guinea": "GN",
                "Guinea-Bissau": "GW",
                "Ivory Coast": "CI",
                "Kenya": "KE",
                "Lesotho": "LS",
                "Liberia": "LR",
                "Libya": "LY",
                "Madagascar": "MG",
                "Malawi": "MW",
                "Mali": "ML",
                "Mauritania": "MR",
                "Mauritius": "MU",
                "Morocco": "MA",
                "Mozambique": "MZ",
                "Namibia": "NA",
                "Niger": "NE",
                "Rwanda": "RW",
                "São Tomé and Príncipe": "ST",
                "Senegal": "SN",
                "Seychelles": "SC",
                "Sierra Leone": "SL",
                "Somalia": "SO",
                "Sudan": "SD",
                "South Sudan": "SS",
                "Swaziland": "SZ",
                "Tanzania": "TZ",
                "Togo": "TG",
                "Tunisia": "TN",
                "Uganda": "UG",
                "Zambia": "ZM",
                "Zimbabwe": "ZW"
            }
            
            # Try to find the country code
            country_code = country_codes.get(country_name)
            if country_code:
                return country_code
                
            # If not found, try to match the first two letters of the country name
            if len(country_name) >= 2:
                return country_name[:2].upper()
                
            return "🌐"  # Default globe emoji
        
        def get_country_flag(country_name: str) -> str:
            """
            Convert country name to flag emoji.
            
            Args:
                country_name (str): Full country name (e.g., "United States", "United Kingdom")
                
            Returns:
                str: Flag emoji
            """
            country_code = get_country_code(country_name)
            
            if country_code == "🌐":
                return country_code
                
            # Convert country code to regional indicator symbols
            # Each letter A-Z is converted to a Unicode regional indicator symbol
            # by adding 127397 to the ASCII code of the letter
            flag = "".join(chr(ord(c) + 127397) for c in country_code)
            
            return flag
        
        # Generate movie cards
        for title, data in sorted(movies.items()):
            imdb_url = f"https://www.imdb.com/title/{data.get('imdb_id', '')}/" if data.get('imdb_id') else "#"
            poster_url = data.get('poster_url') or 'https://via.placeholder.com/300x450?text=No+Poster'
            notes = data.get('notes', '')
            country_name = data.get('country', '')
            flag_emoji = get_country_flag(country_name)
            rating_html = generate_star_rating(data['rating'])
            
            html += f"""
            <div class="movie-card">
                <div class="movie-poster-container">
                    <img class="movie-poster" src="{poster_url}" alt="{title}" loading="lazy">
                    <a href="{imdb_url}" class="imdb-link" target="_blank" rel="noopener">IMDb</a>
                    <a href="https://www.werstreamt.es/film/details/{data.get('imdb_id', '')}/{title.replace(' ', '-').lower()}/" class="watch-link" target="_blank" rel="noopener">
                        <i class="bi bi-play-circle"></i> Watch
                    </a>
                </div>
                <div class="movie-info">
                    <div>
                        <h2 class="movie-title">{title}</h2>
                        <div class="movie-year">
                            {data['year']}
                            <span class="country-flag" title="Country of origin">{flag_emoji}</span>
                        </div>
                        {rating_html}
                    </div>
                </div>
                {f'<div class="movie-notes"><p>{notes}</p></div>' if notes else ''}
            </div>"""
            
        html += """
        </div>
    </div>
</body>
</html>
"""
        
        with open("index.html", "w", encoding='utf-8') as f:
            f.write(html)
            
        print("Website wurde erfolgreich generiert.")

    def _command_exit(self) -> None:
        """Exit the application."""
        print("\nGoodbye!")

    def add_movie_non_interactive(self, title: str) -> None:
        """
        Add a movie without user interaction.
        
        Args:
            title (str): The title of the movie
        """
        try:
            movie_info = self._api.fetch_movie_info(title)
            
            if movie_info is None:
                print(f"Error: Movie '{title}' not found in OMDB database")
                return
                
            if self._storage.add_movie(
                movie_info.title,
                movie_info.year,
                movie_info.rating,
                movie_info.poster_url,
                "",  # Empty note
                movie_info.imdb_id,
                movie_info.country  # Add country
            ):
                print(f"Movie '{movie_info.title}' added successfully")
                print(f"Year: {movie_info.year}")
                print(f"Rating: {movie_info.rating}")
                print(f"Country: {movie_info.country}")
            else:
                print(f"Error: Movie '{movie_info.title}' already exists")
                
        except ConnectionError:
            print("Error: No internet connection available")
        except Exception as e:
            print(f"Error: {str(e)}")

    def run(self) -> None:
        """Run the movie application main loop."""
        while True:
            self._print_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "0":
                self._command_exit()
                break
                
            if choice not in self._commands:
                print("Invalid choice")
                input("\nPress Enter to continue...")
                continue
                
            _, command_func = self._commands[choice]
            
            try:
                command_func()
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                
            input("\nPress Enter to continue...") 