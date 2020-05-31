from parsers.competition import Competition
import requests
from bs4 import BeautifulSoup as bs
import re
from PIL import Image
from io import BytesIO

url = 'https://www.hackerearth.com/ru/challenges/hackathon/'


def parse() -> list:
    parsed_data = []
    page_response = requests.get(url)
    page_response.encoding = 'utf-8'
    page_searcher = bs(page_response.text, features='lxml')
    competitions_containers = select_all_competitions(page_searcher)
    for competitions_container in competitions_containers:
        parsed_data.append(observe_competition(competitions_container))
    return parsed_data


def observe_competition(competition_container_searcher: bs) -> Competition:
    competition_page_link = competition_container_searcher.find('a')['href']
    competition_page = requests.get(competition_page_link)
    competition_page.encoding = 'utf-8'
    competition_page_observer = bs(competition_page.text, features='lxml')
    competition = Competition()
    competition.set_type("Hackaton")
    competition.set_description(get_description(competition_page_observer))
    competition.set_start_date(get_start_date(competition_page_observer))
    competition.set_end_date(get_end_date(competition_page_observer))
    competition.set_location(get_location(competition_page_observer))
    competition.set_link(competition_page_link)
    competition.set_image(get_photo(competition_container_searcher))
    return competition


def select_all_competitions(page_searcher: bs) -> list:
    upcoming_competitions_container = page_searcher.find('div', {'class': 'upcoming challenge-list'})
    if upcoming_competitions_container is None:
        return []
    return upcoming_competitions_container.find_all('div', {'class': 'challenge-card-modern'})


def get_title(observer: bs) -> str:
    competition_title_container = observer.find('span')
    if competition_title_container is None:
        raise Exception("Competition Title Not Found")
    return competition_title_container.text


def get_location(observer: bs) -> str:
    location_container = observer.find("div", {'class': 'location-block'})
    if location_container is None:
        raise Exception("Location Is Not Found")
    return location_container.contents[3].text


def get_start_date(observer: bs) -> str:
    start_date_container = observer.find("div", {'class': 'start-time-block'})
    if start_date_container is None:
        raise Exception("Start Time Is Not Found")
    return start_date_container.contents[3].text


def get_end_date(observer: bs) -> str:
    end_date_container = observer.find("div", {'class': 'end-time-block'})
    if end_date_container is None:
        raise Exception("End Time Is Not Found")
    return end_date_container.contents[3].text


def get_description(observer: bs) -> str:
    try:
        all_info_container = observer.find('div', {'id': 'overview'}).find('div', {'class': 'content'})
        return all_info_container.text
    except:
        return ''


def get_photo(observer: bs) -> object:
    image_tag_str_url = observer.find('div', {'class': 'event-image'})['style']
    url_link = re.search(r"\(\'.*\'\)", image_tag_str_url)
    if url_link is None:
        return None
    url_link = url_link.group()[2:-2]
    photo_response = requests.get(url_link)
    img = Image.open(BytesIO(photo_response.content))
    return img


print(parse())
