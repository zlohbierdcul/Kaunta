from typing import List
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from enum import Enum
import json

# Options
options = FirefoxOptions()
options.add_argument("-headless")

# Driver
driver = Firefox(options=options, service=Service(GeckoDriverManager().install()))


print("Ready!")

class Provider(Enum):
    ANIWATCH = "https://aniwatch.to/search?keyword="
    NINEANIME =   "https://9animetv.to/search?keyword="


def get_driver(url: str, wait_element: str = "film_list"):

    print(f"url: {url} - wait-elem: {wait_element}")
    driver.get(url)
    delay = 10 # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, wait_element)))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    return driver

# Searches the Providers series for the given search term
def find_show(search: str, provider: Provider = Provider.ANIWATCH) -> list(tuple()):
    if (provider == Provider.ANIWATCH):
        driver = get_driver(Provider.ANIWATCH.value + search)
    if (provider == Provider.NINEANIME):
        driver = get_driver(Provider.NINEANIME.value + search)
    shows = driver.find_elements(By.CLASS_NAME, "film-poster-ahref")
    result = list()
    for show in shows:
        result.append((show.get_attribute("oldtitle"), show.get_attribute("href")))
    return result


def find_season(search_url: str) -> list(tuple()):
    driver = get_driver(search_url)
    seasons = driver.find_elements(By.CLASS_NAME, "os-item")
    season_links = list()
    if len(seasons) > 0:    
        for season in seasons:
            title = season.find_element(By.CLASS_NAME, "title")
            if title != None:
                season_links.append((title.text, season.get_attribute("href")))
    else:
        watch_btn = driver.find_element(By.CLASS_NAME, "btn-play")
        season_links.append(("Season 1", watch_btn.get_attribute("href")))
    return format_links(season_links)
    

def find_episodes(series_url: str) -> dict:
    driver = get_driver(series_url, "ssl-item")
    episodes = driver.find_elements(By.CLASS_NAME, "ep-item")
    show_name = find_show_name(driver)
    episode_dict = dict()
    episode_dict[show_name] = {}
    for index, episode in enumerate(episodes):
        episode_dict[show_name][index + 1] = {
            "Titel": episode.get_attribute("title"),
            "Filler": True if "filler" in episode.get_attribute("class") else False,
            "URL": episode.get_attribute("href")
        }
    return episode_dict


def find_show_name(driver) -> str:
    show_details = driver.find_element(By.CLASS_NAME, "anisc-detail")
    show_name_wrapper = show_details.find_element(By.CLASS_NAME, "dynamic-name")
    return show_name_wrapper.get_attribute("title")
    


def format_links(links: List[tuple]) -> List[tuple]:
    for index, (name, link) in enumerate(links):
        print(f"link: {link}")
        if ("/watch/" not in link):
            new_link = link.replace(".to", ".to/watch")
        else:
            new_link = link
        links[index] = (name, new_link)
    return links

if __name__ == "__main__":
    links = [("Season 1", 'https://aniwatch.to/kaguya-sama-love-is-war-123'), ("Season 2", 'https://aniwatch.to/kaguya-sama-love-is-war-season-2-23'), ("Season 3", 'https://aniwatch.to/kaguya-sama-love-is-war-ultra-romantic-17224')]
    print(format_links(links))

    
