import re
import requests
from bs4 import BeautifulSoup
from .models import Vacancy

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
        job = Vacancy(
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

def parse_NoFluffJobs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract total count of found offers
    count_limit = 0
    count_elem = soup.find(string=re.compile(r'^\s*\(\d+\)\s*$'))
    if count_elem:
        try:
            count_limit = int(count_elem.strip().strip('()'))
        except ValueError:
            pass

    offer_cards = soup.find_all('a', class_='posting-list-item')
    jobs = []

    for card in offer_cards[:count_limit] if count_limit > 0 else offer_cards:
        city_elem = card.find('nfj-posting-item-city')
        location = city_elem.text.strip() if city_elem else 'N/A'
        
        job = Vacancy(
            link = 'https://nofluffjobs.com' + card.get('href', ''),
            title = card.find('h3', class_='posting-title__position').text.strip(),
            company = card.find('h4', class_='company-name').text.strip(),
            location = location,
            salary = card.find('nfj-posting-item-salary').find('span').text.strip().replace('\xa0', ' ') if card.find('nfj-posting-item-salary') else 'Undisclosed',
            cards = [tag.text.strip() for tag in card.find('nfj-posting-item-tiles').find_all('span', class_='posting-tag')] if card.find('nfj-posting-item-tiles') else [],
            is_remote = 'Remote' in location,
            is_one_click = False,
            description = None,
            cv_code = None
        )
        jobs.append(job)
    return jobs

def parse_NoFluffJobs_vacancy_description(vacancy_url):
    response = requests.get(vacancy_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = soup.find('section', id='posting-description').text.strip()
    return description

def parse_job_vacancies(url):
    if "justjoin.it" in url:
        return parse_JustJoinIt(url)
    elif "nofluffjobs.com" in url:
        return parse_NoFluffJobs(url)
    else:
        raise ValueError("Unsupported URL")

def parse_job_vacancy_description(url):
    if "justjoin.it" in url:
        return parse_JustJoinIt_vacancy_description(url)
    elif "nofluffjobs.com" in url:
        return parse_NoFluffJobs_vacancy_description(url)
    else:
        raise ValueError("Unsupported URL")
