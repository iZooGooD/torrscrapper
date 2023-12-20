# Torrscrapper

Torrscrapper is a web scraping application designed to extract torrents for various types of media, such as games, movies, and more. It enables users to search for torrents and view the results without the distraction of ads.

## Getting Started

These instructions will help you set up and run the Torrscrapper application on your local machine.

### Prerequisites

Before you begin, ensure you have the following software installed:

- Python 3.x ([Download Python](https://www.python.org/downloads/))
- Django ([Download Django](https://www.djangoproject.com/download/))

### Start Searching

Run the below commands in the project directory:
1. `pip install -r requirements.txt`
2. `python manage.py runserver`

Now visit http://127.0.0.1:8000/ and start searching for your torrents without any ads.

## Features

### Advanced Scraping Techniques
1. **Concurrent Scraping**: Utilizes Python modules like `asyncio` to perform multiple web scraping requests simultaneously, significantly reducing the total time spent in scraping.
2. **Cloudflare Bypass**: Employs the `cloudscrape` module to effectively bypass Cloudflare security measures, ensuring reliable access to torrent sites.

### Comprehensive Torrent Databases
3. **Games Database**: Features a pre-built SQLite database containing links to magnet files for over 3,000 popular games.
4. **Movies Database**: Comes with a pre-built SQLite database housing magnet links for more than 10,000 movies.

### Ongoing Enhancements
- **Database Updates**: Ongoing work includes updating the SQLite databases using Python scripts to ensure the latest and most popular content is readily available.
- **Site Support Expansion**: Planning  to extend support to additional torrent sites