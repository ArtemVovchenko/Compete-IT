import requests
from bs4 import BeautifulSoup as bs
from parsers.competition import Competition
import svglib

locations = ["LIVE CODING CHALLENGE", "ONLINE", "ONSITE HACKATHON", 'ONLINE CREATIVE CHALLENGE']
url_competitions_catalog = '/hackathons-and-challenges'
url_base = 'https://challengerocket.com'
url_tail = '.html'


def parse() -> list:
    all_parsed_competitions = []
    url = url_base + url_competitions_catalog + url_tail
    page = get_page(url)
    competitions = select_all_competitions(page)
    all_parsed_competitions.append(observe_competitions(competitions))

    for i in range(1, 10):
        url = url_base + url_competitions_catalog + f",{i}" + url_tail
        all_parsed_competitions.append(select_all_competitions(get_page(url)))

    return all_parsed_competitions


def get_page(url: str) -> str:
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    return response.text


def select_all_competitions(content: str):
    searcher = bs(content, features='lxml')
    all_info = searcher.find(name='ul', attrs={'class': 'list'})
    return all_info.find_all(name='li')


def observe_competitions(competitions: list) -> list:   #TODO: Add SVG -> PNG CONVERTATION AND SAVING TO COMPETITION CLASS
    competitions_list = []
    for competition_info in competitions:
        competition_location = competition_info.find("dd", {"class": "icon-location"})
        competition_title = competition_info.find('h2').text
        if competition_location is None:
            continue

        if not str(competition_location.text).upper() in locations:
            continue

        competition_type = None

        if competition_location.text.upper() in ["LIVE CODING CHALLENGE", "ONLINE"]:
            competition_type = 'contest'
        else:
            competition_type = 'hackaton'

        competition_page_url = competition_info.find('a')
        competition_description = get_description(url_base + competition_page_url['href'] + url_tail)
        competition_date = competition_info.find('dd', {'class': 'icon-date'}).text
        class_competition = Competition()
        class_competition.set_location(competition_location)
        class_competition.set_start_date(competition_date)
        class_competition.set_description(competition_description)
        class_competition.set_title(competition_title)
        class_competition.set_type(competition_type)
        competitions_list.append(class_competition)

    return competitions_list



def get_description(competition_page_url: str) -> str:
    response = requests.get(competition_page_url)
    response.encoding = 'utf-8'
    searcher = bs(response.text, features='lxml')
    return searcher.find('section', {'class', 'challenge-description'}).find("div", {'class': 'text'}).text





