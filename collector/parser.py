import requests
from bs4 import BeautifulSoup
import json
from .models import JustJoinItVacancy

url = 'https://justjoin.it/job-offers/warszawa/python?experience-level=junior&orderBy=DESC&sortBy=newest'

def parse_JustJoinIt_vacancy_description(vacancy_url):
    response = requests.get(vacancy_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = soup.find('div', class_='MuiStack-root mui-eorvb9').text.strip()
    return description

def parse_JustJoinIt(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    offer_cards = soup.find_all('a', class_='offer-card')
    jobs = []

    for card in offer_cards:
        remote_badge = card.find('span', class_='mui-l362hr')
        job = JustJoinItVacancy(
            link = 'https://justjoin.it' + card.get('href', ''),
            title = card.find('h3').text.strip(),
            company = card.find('p', class_='MuiTypography-root').text.strip(),
            location = ', '.join([loc.text.strip() for loc in card.find_all('span', class_='mui-1o4wo1x')]) if card.find_all('span', class_='mui-1o4wo1x') else 'N/A',
            salary = ' '.join([tag.text.strip() for tag in card.find_all('span', class_='MuiTypography-root') if tag.text.strip().replace(' ', '').isdigit() or 'PLN' in tag.text.strip() or 'month' in tag.text.strip()]) if card.find_all('span', class_='MuiTypography-root') else 'Undisclosed',
            cards = list(dict.fromkeys([skill.text.strip() for skill in card.find_all('div', class_='mui-jikuwi') if skill.text.strip()])),
            is_remote = remote_badge is not None,
            is_one_click = '1-click Apply' in list(dict.fromkeys([skill.text.strip() for skill in card.find_all('div', class_='mui-jikuwi') if skill.text.strip()])),
            description = None,
            cv_code = None
        )
        jobs.append(job)
    return jobs
