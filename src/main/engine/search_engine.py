from typing import List
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from enum import Enum
import json

# Options
options = FirefoxOptions()
options.add_argument("-headless")

# Driver
driver = Firefox(options)      
print("Ready!")

class Provider(Enum):
    ANIWATCH = "https://aniwatch.to/search?keyword="
    NINEANIME =   "https://9animetv.to/search?keyword="
        
        
def get_driver(url: str, wait_element: str = "film_list"):
    driver.get(url)

    delay = 2 # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, wait_element)))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    return driver

# Searches the Providers series for the given search term
def find_show(search: str, provider: Provider = Provider.ANIWATCH) -> list(tuple()):
    match (provider):
        case Provider.ANIWATCH:
            driver = get_driver(Provider.ANIWATCH.value + search)
        case Provider.NINEANIME:
            driver = get_driver(Provider.NINEANIME.value + search)
    shows = driver.find_elements(By.CLASS_NAME, "film-poster-ahref")
    result = list()
    for show in shows:
        result.append((show.get_attribute("oldtitle"), show.get_attribute("href")))
    return result


def find_season(search_url: str) -> list(tuple()):
    driver = get_driver(search_url)
    seasons = driver.find_elements(By.CLASS_NAME, "os-item")
    result = list()
    for season in seasons:
        title = season.find_element(By.CLASS_NAME, "title")
        if title != None:
            result.append((title.text, season.get_attribute("href")))
    return result
    

def find_episodes(series_url: str) -> dict():
    driver = get_driver(series_url, "ssl-item")
    episodes = driver.find_elements(By.CLASS_NAME, "ep-item")
    episode_dict = dict()
    for index, episode in enumerate(episodes):
        episode_dict[index + 1] = {
            "Titel": episode.get_attribute("title"),
            "Filler": True if "filler" in episode.get_attribute("class") else False,
            "URL": episode.get_attribute("href")
        }
    return episode_dict


if __name__ == "__main__":
    while True:  
        str = input()
        results = find_episodes(str)
        with open("out.json", "+a") as f:
            json.dump(results, f)
        print("fin")
    