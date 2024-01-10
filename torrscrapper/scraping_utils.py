from bs4 import BeautifulSoup
import cloudscraper
from .constants import SiteURLs
import logging
from datetime import datetime
import time
import asyncio
import aiohttp
import humanize
import urllib.parse
import sys

# Create a logger object
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# File handler for outputting log messages to a file
file_handler = logging.FileHandler('scraping_logs.log', encoding='utf-8')
file_handler.setFormatter(formatter)

# Stream handler for outputting log messages to the console
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Adding handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

## global variables
scraper = cloudscraper.create_scraper(browser='chrome')

def scrape_data(keywords, selected_sites):
    site_scrapers = {
        '1337x': get_1337x_torrents,
        'pirate_bay': get_pirate_bay_torrents
    }
    combined_results = []

    overall_start_time = time.time()
    logging.info("---------------------------------------------------")
    print("Starting the scraping session")
    logging.info(" 🚀Starting the scraping session")

    # If no sites are selected, scrape from all sites
    if not selected_sites:
        selected_sites = site_scrapers.keys()

    for index, site_key in enumerate(selected_sites, start=1):
        if site_key in site_scrapers:
            scraper_function = site_scrapers[site_key]
            start_time = time.time()
        logging.info(f"🌐 Site #{index} - Starting scraping for site: {site_key}")

        # Append results from each site to the combined_results list
        combined_results.extend(scraper_function(keywords, index))

        end_time = time.time()
        time_taken = end_time - start_time
        logging.info(f"Site #{index} - Completed scraping. Time taken: {time_taken:.2f} seconds")
        logging.info(f"Site #{index} - --------------------------------")

    overall_end_time = time.time()
    overall_time_taken = overall_end_time - overall_start_time
    logging.info(f"🎉 Ending the scraping session. Total time taken: {overall_time_taken:.2f} seconds")
    logging.info(f"Overall collected {len(combined_results)} torrents")
    logging.info("---------------------------------------------------")

    return sort_torrents_by_seeds(combined_results)

# Function to sort torrents by the number of seeds
def sort_torrents_by_seeds(torrents):
    return sorted(torrents, key=lambda x: int(x['seeds']), reverse=True)

async def fetch_magnet(session, magnet_url, torrent):
    async with session.get(magnet_url) as response:
        if response.status == 200:
            magnet_content = await response.read()
            magnet_soup = BeautifulSoup(magnet_content, 'html.parser')
            magnet_link = magnet_soup.find('a', href=lambda href: href and 'magnet:?' in href)
            if magnet_link:
                torrent['magnet'] = magnet_link.get('href')
            else:
                torrent['magnet'] = ""
        else:
            print(f"Error fetching magnet link for {torrent['title']}")

async def get_1337x_torrents_async(keywords, torrents):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for torrent in torrents:
            magnet_url = torrent['magnet']
            if magnet_url:
                task = asyncio.create_task(fetch_magnet(session, magnet_url, torrent))
                tasks.append(task)

        # Limiting the number of parallel requests to 5 for now
        chunk_size = 5
        for i in range(0, len(tasks), chunk_size):
            await asyncio.gather(*tasks[i:i + chunk_size])

def get_1337x_torrents(keywords, index):
    torrents = []
    search_url = SiteURLs.X1337_BASE_URL + '/search/' + keywords + '/1/'
    response = scraper.get(search_url)
    if response.status_code == 200:
        logging.info(f"Site #{index} - Initial request to site {search_url} was successful")
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                name_col = cols[0].find_all('a', href=True)
                if len(name_col) >= 2 and name_col[1]['href'].startswith('/torrent/'):
                    name = name_col[1].text.strip()
                    href = SiteURLs.X1337_BASE_URL + name_col[1]['href']
                    seeds = cols[1].text
                    leeches = cols[2].text
                    size_element = cols[4].find(text=True, recursive=False).strip()
                    size = size_element if size_element else None
                    torrent = {
                        'title': name,
                        'magnet': href,
                        'seeds': seeds,
                        'peers': leeches,
                        'size': size
                    }
                    torrents.append(torrent)

        asyncio.run(get_1337x_torrents_async(keywords, torrents))  # Call the asynchronous function
        logging.info(f"Site #{index} - Collected {len(torrents)} torrents")
        return torrents
    else:
        logging.error(f"Failed to scrape 1337x. Status code: {response.status_code}")
        return []

def create_magnet_pirate_bay(info_hash, name):
    """
    Generates a magnet link for a torrent from The Pirate Bay.

    Pirate Bay uses custom JavaScript to generate magnet links for its torrents.
    This function replicates that functionality in Python, creating a magnet link
    that includes the necessary trackers.

    Parameters:
    info_hash (str): The information hash of the torrent.
    name (str): The name of the torrent.

    Returns:
    str: A magnet link for the given torrent.
    """

    trackers = [
        'udp://tracker.coppersurfer.tk:6969/announce',
        'udp://tracker.openbittorrent.com:6969/announce',
        'udp://9.rarbg.to:2710/announce',
        'udp://9.rarbg.me:2780/announce',
        'udp://9.rarbg.to:2730/announce',
        'udp://tracker.opentrackr.org:1337',
        'http://p4p.arenabg.com:1337/announce',
        'udp://tracker.torrent.eu.org:451/announce',
        'udp://tracker.tiny-vps.com:6969/announce',
        'udp://open.stealth.si:80/announce'
    ]

    tracker_str = ''.join(['&tr=' + urllib.parse.quote(tracker) for tracker in trackers])
    magnet_link = f'magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(name)}{tracker_str}'

    return magnet_link

def get_pirate_bay_torrents(keywords, index):
    torrents = []
    search_url = SiteURLs.PIRATE_BAY_BASE_URL + 'q=' + keywords
    response = scraper.get(search_url)

    if response.status_code == 200:
        logging.info(f"Site #{index} - Initial request to site {search_url} was successful")
        json_data = response.json()
        for item in json_data:
            name = item.get("name")
            info_hash = item.get("info_hash")
            seeders = item.get("seeders")
            leechers = item.get("leechers")
            size = humanize.naturalsize(int(item.get("size")), binary=True)  # Converts bytes to human-readable format
            torrent = {
                'title': name,
                'seeds': seeders,
                'peers': leechers,
                'magnet': create_magnet_pirate_bay(info_hash, name),
                'size': size
            }
            torrents.append(torrent)
        logging.info(f"Site #{index} - Collected {len(torrents)} torrents")
    else:
        logging.error(f"Site #{index} - Failed to scrape Pirate Bay. Status code: {response.status_code}")

    return torrents