import re
import requests
import time
import json
from bs4 import BeautifulSoup
from .models import Vacancy
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page_content_with_browser(url):
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = uc.Chrome(options=options)
    try:
        driver.get(url)
        
        WebDriverWait(driver, 35).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        WebDriverWait(driver, 35).until(
            EC.all_of(
                EC.presence_of_element_located((By.TAG_NAME, "footer"))
            )
        )
        return driver.page_source
    finally:
        driver.quit()

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
            cv_code = None,
            cover_letter = None
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
            cv_code = None,
            cover_letter = None
        )
        jobs.append(job)
    return jobs

def parse_NoFluffJobs_vacancy_description(vacancy_url):
    response = requests.get(vacancy_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    description = soup.find('section', id='posting-description').text.strip()
    requirements = soup.find('div', id='posting-requirements').text.strip()
    requirements2 = soup.find('section', {'data-cy-section': 'JobOffer_Requirements'}).text.strip()
    return requirements + "\n\n" + requirements2 + "\n\n" + description

def parse_theProtocolIt(url):
    #TODO: review it better cause it vibecoded and might be shitty
    html = get_page_content_with_browser(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if not next_data_script:
        return []
    
    try:
        data = json.loads(next_data_script.string)
        offers_data = data['props']['pageProps']['offersResponse']['offers']
    except (KeyError, json.JSONDecodeError, TypeError):
        return []

    jobs = []
    for offer in offers_data:
        # Construct tags
        tags = offer.get('technologies', [])
        
        # Location handling
        workplaces = offer.get('workplace', [])
        location = "N/A"
        if workplaces:
            location = ", ".join([w.get('location', '') for w in workplaces])
        
        # Salary handling
        salary_data = offer.get('salary')
        salary = "Undisclosed"
        if salary_data:
            from_val = salary_data.get('from')
            to_val = salary_data.get('to')
            currency = salary_data.get('currency', '')
            type_val = salary_data.get('type', '')
            if from_val and to_val:
                salary = f"{from_val} - {to_val} {currency} {type_val}"
            elif from_val:
                salary = f"{from_val} {currency} {type_val}"
        
        job = Vacancy(
            link = "https://theprotocol.it/praca/" + offer.get('offerUrlName', ''),
            title = offer.get('title', 'N/A'),
            company = offer.get('employer', 'N/A'),
            location = location,
            salary = salary,
            cards = tags,
            is_remote = 'zdalna' in [m.lower() for m in offer.get('workModes', [])],
            is_one_click = offer.get('badges', {}).get('isQuickApply', False),
            description = None,
            cv_code = None,
            cover_letter = None
        )
        jobs.append(job)
    return jobs

def parse_BulldogJob(url):
    #TODO: vibecoded, review it
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if not next_data_script:
        return []
    
    try:
        data = json.loads(next_data_script.string)
        jobs_data = data['props']['pageProps']['jobs']
    except (KeyError, json.JSONDecodeError, TypeError):
        return []

    jobs = []
    for job_data in jobs_data:
        salary_data = job_data.get('denominatedSalaryLong')
        salary = "Undisclosed"
        if salary_data and not salary_data.get('hidden'):
            money = salary_data.get('money', '')
            currency = salary_data.get('currency', '')
            salary = f"{money} {currency}"
        
        job = Vacancy(
            link = "https://bulldogjob.pl/companies/jobs/" + job_data.get('id', ''),
            title = job_data.get('position', 'N/A'),
            company = job_data.get('company', {}).get('name', 'N/A'),
            location = job_data.get('city', 'N/A'),
            salary = salary,
            cards = job_data.get('technologyTags', []),
            is_remote = job_data.get('remote', False),
            is_one_click = False,
            description = None,
            cv_code = None,
            cover_letter = None
        )
        jobs.append(job)
    return jobs

def parse_BulldogJob_vacancy_description(vacancy_url):
    #TODO: vibecoded, review it
    response = requests.get(vacancy_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if next_data_script:
        try:
            data = json.loads(next_data_script.string)
            
            # Deep search for 'job' object
            def find_key(obj, key):
                if isinstance(obj, dict):
                    if key in obj:
                        return obj[key]
                    for k, v in obj.items():
                        result = find_key(v, key)
                        if result:
                            return result
                elif isinstance(obj, list):
                    for item in obj:
                        result = find_key(item, key)
                        if result:
                            return result
                return None

            job_details = find_key(data, 'job')
            if job_details:
                desc_html = job_details.get('details') or job_details.get('description')
                if desc_html:
                    desc_soup = BeautifulSoup(desc_html, 'html.parser')
                    return desc_soup.get_text(separator='\n').strip()
        except (KeyError, json.JSONDecodeError, TypeError):
            pass

    description_elem = soup.find('div', id='job-description')
    if description_elem:
        return description_elem.get_text(separator='\n').strip()
        
    return "Description not found."

def parse_theProtocolIt_vacancy_description(vacancy_url):
    #TODO: review it better cause it vibecoded and might be shitty
    html = get_page_content_with_browser(vacancy_url)
    soup = BeautifulSoup(html, 'html.parser')
    
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if next_data_script:
        try:
            data = json.loads(next_data_script.string)
            offer_details = data['props']['pageProps']['offer']
            sections = offer_details.get('jsonSections', [])
            
            content_parts = []
            
            def process_section(section):
                title = section.get('title')
                if title:
                    content_parts.append(f"\n{title}")
                
                model = section.get('model')
                if model:
                    m_type = model.get('modelType')
                    if m_type == 'multi-paragraph':
                        content_parts.extend([p for p in model.get('paragraphs', []) if p.strip()])
                    elif m_type == 'bullets':
                        content_parts.extend([f"• {b}" for b in model.get('bullets', []) if b.strip()])
                    elif m_type == 'open-dictionary':
                        items = model.get('customItems', [])
                        if not items:
                            items = model.get('items', [])
                        content_parts.extend([item.get('name') for item in items if item.get('name')])
                
                # Process sub-sections recursively
                for sub in section.get('subSections', []) or []:
                    process_section(sub)

            for section in sections:
                process_section(section)
                
            result = "\n".join(content_parts).strip()
            if result:
                return result
        except (KeyError, json.JSONDecodeError, TypeError):
            pass

    # Fallback to BeautifulSoup if JSON fails or is incomplete
    description_elem = soup.find('div', attrs={'data-cy': 'job-description'}) or soup.find('section', id='job-description')
    requirements_elem = soup.find('div', attrs={'data-cy': 'job-requirements'}) or soup.find('section', id='job-requirements')
    
    content = ""
    if requirements_elem:
        content += "REQUIREMENTS:\n" + requirements_elem.text.strip() + "\n\n"
    if description_elem:
        content += "DESCRIPTION:\n" + description_elem.text.strip()
        
    return content if content else "Description not found."

def parse_job_vacancies(url):
    if "justjoin.it" in url:
        return parse_JustJoinIt(url)
    elif "nofluffjobs.com" in url:
        return parse_NoFluffJobs(url)
    elif "theprotocol.it" in url:
        return parse_theProtocolIt(url)
    elif "bulldogjob.pl" in url:
        return parse_BulldogJob(url)
    else:
        raise ValueError("Unsupported URL")

def parse_job_vacancy_description(url):
    if "justjoin.it" in url:
        return parse_JustJoinIt_vacancy_description(url)
    elif "nofluffjobs.com" in url:
        return parse_NoFluffJobs_vacancy_description(url)
    elif "theprotocol.it" in url:
        return parse_theProtocolIt_vacancy_description(url)
    elif "bulldogjob.pl" in url:
        return parse_BulldogJob_vacancy_description(url)
    else:
        raise ValueError("Unsupported URL")
