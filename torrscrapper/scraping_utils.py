# app_name/scraping_utils.py

import requests
from bs4 import BeautifulSoup
import cloudscraper
from .constants import SiteURLs
import logging
from datetime import datetime
import time

# Configure the logging
logging.basicConfig(
    filename='scraping_logs.log',  # Name of the log file
    level=logging.INFO,  # Set the logging level (change it as needed)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

## global variables
scraper = cloudscraper.create_scraper(browser='chrome')

def scrape_data(url, keywords):
    if url == SiteURLs.X1337_BASE_URL:
        return get_1337x_torrents(keywords)

def get_1337x_torrents(keywords):
    start_time = time.time()
    torrents = []
    search_url = SiteURLs.X1337_BASE_URL + '/search/' + keywords + '/1/'
    response = scraper.get(search_url)
    if response.status_code == 200:
        logging.info(f"---------------------------------------------------")
        logging.info(f"Starting the scrapper")
        logging.info(f"Initial request to site {search_url} was successful")
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                name_col = cols[0].find_all('a', href=True)
                if len(name_col) >= 2 and name_col[1]['href'].startswith('/torrent/'):
                    name = name_col[1].text.strip()
                    href = SiteURLs.X1337_BASE_URL + name_col[1]['href']
                    magnet_response = scraper.get(href)
                    if magnet_response.status_code == 200:
                        magnet_soup = BeautifulSoup(magnet_response.content, 'html.parser')
                        magnet_link = magnet_soup.find('a', href=lambda href: href and 'magnet:?' in href)
                        if magnet_link:
                            magnet_href = magnet_link.get('href')
                        else:
                            magnet_href = "Magnet link not found"
                    else:
                        print(f"Error fetching magnet link for {name}")
                        magnet_href = "Error fetching magnet"

                    seeds = cols[1].text
                    leeches = cols[2].text
                    size_element = cols[4].find(text=True, recursive=False).strip()
                    size = size_element if size_element else None

                    torrent = {
                        'title': name,
                        'magnet': magnet_href,
                        'seeds': seeds,
                        'peers': leeches,
                        'size': size
                    }
                    torrents.append(torrent)
        logging.info(f"Collected {len(torrents)} torrents")
        end_time = time.time()  # Record the end time
        time_taken = end_time - start_time  # Calculate time taken
        logging.info(f"Time taken for scraping: {time_taken:.2f} seconds")
        logging.info(f"Ending the scrapper")
        logging.info(f"---------------------------------------------------")
        return torrents
    else:
        print(f"Error in initial request. Status code: {response.status_code}")
        print(f"Maybe site name/extenion has changed ?")
        logging.error(f"Error in initial request. Status code: {response.status_code}")
        logging.error("Maybe site name/extension has changed?")
        return []