#!/usr/bin/env python3

"""
Haupteinstiegspunkt für das Movie Management System.
Unterstützt verschiedene Storage-Typen basierend auf der Dateiendung.
"""

import os
import argparse
from typing import Union
from src.movie_app import MovieApp
from src.storage.implementations.json_storage import StorageJson
from src.storage.implementations.csv_storage import StorageCsv
from src.storage.istorage import IStorage
from src.config.config import DEFAULT_JSON_FILE


def determine_storage(file_path: str) -> IStorage:
    """
    Bestimmt den Storage-Typ basierend auf der Dateiendung.
    
    Args:
        file_path (str): Pfad zur Storage-Datei
        
    Returns:
        IStorage: Passende Storage-Implementation
        
    Raises:
        ValueError: Wenn die Dateiendung nicht unterstützt wird
    """
    # Dateiendung extrahieren (kleingeschrieben)
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    # Storage-Typ basierend auf Endung wählen
    if ext == '.json' or ext == '':  # Default zu JSON wenn keine Endung
        return StorageJson(file_path)
    elif ext == '.csv':
        return StorageCsv(file_path)
    else:
        raise ValueError(
            f"Nicht unterstütztes Dateiformat: {ext}\n"
            "Unterstützte Formate: .json, .csv oder keine Endung"
        )


def parse_args() -> argparse.Namespace:
    """
    Parst die Kommandozeilenargumente.
    
    Returns:
        argparse.Namespace: Geparste Argumente
    """
    parser = argparse.ArgumentParser(
        description="Movie Management System - Verwalten Sie Ihre Filmsammlung",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python main.py movies.json    # Verwendet JSON-Storage
  python main.py data.csv       # Verwendet CSV-Storage
  python main.py moviedb        # Verwendet JSON-Storage (Standard)
        """
    )
    
    parser.add_argument(
        'storage_file',
        nargs='?',
        default=DEFAULT_JSON_FILE,
        help='Pfad zur Storage-Datei (.json oder .csv)'
    )
    
    return parser.parse_args()


def main():
    """
    Hauptfunktion, die die Movie-Anwendung initialisiert und startet.
    Verarbeitet Kommandozeilenargumente für verschiedene Storage-Typen.
    """
    # Kommandozeilenargumente parsen
    args = parse_args()
    
    try:
        # Storage basierend auf Dateiendung initialisieren
        storage = determine_storage(args.storage_file)
        
        # Movie-Anwendung erstellen und starten
        app = MovieApp(storage_type="json", storage_path=args.storage_file)
        app.run()
        
    except ValueError as e:
        print(f"Fehler: {str(e)}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}")


if __name__ == "__main__":
    main() 