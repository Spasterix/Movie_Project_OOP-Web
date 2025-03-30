# 🎬 Movie Collection Manager

A modern Python-based movie collection management system with a beautiful web interface. Built with clean architecture and object-oriented principles.

## ✨ Features

- 🎯 **Movie Management**: Add, update, and organize your movie collection
- 🌐 **OMDB Integration**: Automatic movie information fetching
- 🎨 **Beautiful UI**: Responsive web interface with modern design
- 🎭 **Rich Metadata**: Store ratings, notes, and streaming availability
- 🎪 **Multiple Storage Options**: JSON and CSV support
- 🔍 **Smart Search**: Find movies by title, year, or rating
- 📊 **Statistics**: Track your collection's metrics
- 🌍 **International Support**: Country flags and multi-language support
- 🔗 **Streaming Integration**: Direct links to WerStreamt.es
- 📱 **Mobile Friendly**: Fully responsive design

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/Spasterix/Movie_Project_OOP-Web.git
cd Movie_Project_OOP-Web
```

2. **Get your OMDB API Key**
- Visit [OMDB API](http://www.omdbapi.com/apikey.aspx)
- Register for a free API key
- You will receive your key via email

3. **Create and configure environment file**
Create a `.env` file in the project root:
```bash
# OMDB API Configuration
OMDB_API_KEY=your_api_key_here  # Replace with your actual API key

# Website Configuration
WEBSITE_TITLE=My Movie Collection
WEBSITE_OUTPUT=index.html
```

4. **Install dependencies**
```bash
pip install -e .
```

5. **Run the application**
```bash
python src/main.py
```

6. **View your collection**
Open `index.html` in your browser

## 🔐 Environment Configuration

The application uses a `.env` file for configuration. Create this file in the project root with the following variables:

```env
# OMDB API Configuration
OMDB_API_KEY=your_api_key_here  # Get your key from http://www.omdbapi.com/apikey.aspx

# Website Configuration
WEBSITE_TITLE=My Movie Collection
WEBSITE_OUTPUT=index.html
```

> ⚠️ **Important**: 
> - Never commit your `.env` file to version control. It's already included in `.gitignore`.
> - Each user must obtain their own OMDB API key from [OMDB API](http://www.omdbapi.com/apikey.aspx).
> - The free API key has a daily request limit of 1000 requests.

## 🏗️ Project Structure

```
movie_project_oop/
├── .env                    # Environment configuration (create this)
├── config/                 # Configuration files
│   └── config.py
├── data/                  # Data storage
│   └── movies.json
├── src/                   # Source code
│   ├── storage/          # Storage implementations
│   │   ├── implementations/
│   │   │   ├── json_storage.py
│   │   │   └── csv_storage.py
│   │   └── istorage.py
│   ├── main.py           # Application entry point
│   ├── movie_api.py      # OMDB API integration
│   └── movie_app.py      # Core application logic
├── tests/                # Test suite
│   ├── test_movie_system.py
│   └── test_storage.py
├── setup.py             # Package configuration
└── README.md           # Documentation
```

## 🛠️ Development

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- OMDB API key
- python-dotenv package

### Running Tests
```bash
python -m unittest discover tests -v
```

### Code Style
- Follows PEP 8 guidelines
- Type hints throughout the codebase
- Comprehensive docstrings
- Clean architecture principles

## 📦 Storage Options

### JSON Storage (Default)
- Human-readable format
- Supports rich metadata
- Easy to backup and version control

### CSV Storage
- Simple tabular format
- Easy to import/export
- Compatible with spreadsheet software

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OMDB API for movie data
- WerStreamt.es for streaming availability
- Bootstrap for the beautiful UI components
- All contributors and users of this project

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers. 
