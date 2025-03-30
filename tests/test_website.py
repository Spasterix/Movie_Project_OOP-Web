#!/usr/bin/env python3
"""
Test-Skript zum Hinzufügen von 20 Filmen und Generieren der Website.
"""

import time
from src.movie_app import MovieApp

def main():
    """Füge 20 Filme hinzu und generiere die Website."""
    
    # Liste bekannter Filme
    movies = [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Pulp Fiction",
        "Fight Club",
        "Inception",
        "The Matrix",
        "Goodfellas",
        "The Silence of the Lambs",
        "Schindler's List",
        "Forrest Gump",
        "The Lord of the Rings: The Fellowship of the Ring",
        "Star Wars: Episode IV - A New Hope",
        "Back to the Future",
        "The Terminator",
        "Jurassic Park",
        "Indiana Jones and the Raiders of the Lost Ark",
        "Alien",
        "The Lion King",
        "Gladiator"
    ]
    
    # Initialisiere die App
    app = MovieApp()
    
    # Füge jeden Film hinzu
    for movie in movies:
        print(f"\nFüge Film hinzu: {movie}")
        app.add_movie_non_interactive(movie)
        time.sleep(1)  # Kleine Pause zwischen API-Aufrufen
    
    # Generiere die Website
    print("\nGeneriere Website...")
    app._command_generate_website()
    print("\nFertig! Öffne index.html im Browser, um das Ergebnis zu sehen.")

if __name__ == "__main__":
    main() 