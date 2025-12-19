from collector.parser import parse_job_vacancies, parse_job_vacancy_description
from dataclasses import asdict
import requests
import os
from generator.generator import ask_openai, ask_openai_cover_letter
from database.database import init_db, save_data, data_exists, delete_old_vacancies

urls = ['https://justjoin.it/job-offers/warszawa/python?experience-level=junior&orderBy=DESC&sortBy=newest', #python, junior, Warszawa
        'https://justjoin.it/job-offers/remote/python?experience-level=junior&orderBy=DESC&sortBy=newest', #python, junior, Remote
        'https://nofluffjobs.com/pl/praca-zdalna/Python?utm_source=google&utm_medium=cpc&utm_campaign=PL_PL_srhbrand1&utm_id=12127570708&gad_source=1&gad_campaignid=12127570708&gbraid=0AAAAADJ4zV3nIRZXNCTw9hmn74kNFwCo2&gclid=Cj0KCQiAxonKBhC1ARIsAIHq_lunm2sFKicAOeCSaPat1mRvKo1NOanykhLwhhC5o58SpJEHOVNwsZAaAhN3EALw_wcB&criteria=city%3Dwarszawa%20%20jobLanguage%3Dpl,en,ru%20seniority%3Djunior', #python, junior, Warszawa or remote
        'https://theprotocol.it/filtry/python;t/junior;p/warszawa;wp?sort=date', #python, junior, Warszawa
        'https://theprotocol.it/filtry/python;t/junior;p/zdalna;rw?sort=date', #python, junior, Remote
        'https://bulldogjob.pl/companies/jobs/s/skills,Python/experienceLevel,junior/city,Warszawa', #python, junior, Warszawa
        'https://bulldogjob.pl/companies/jobs/s/skills,Python/experienceLevel,junior/city,Remote' #python, junior, Remote
]

init_db()

jobs = []
for url in urls:
    jobs.extend(parse_job_vacancies(url))

for job in jobs:
    if not data_exists(job.link):
        job.description = parse_job_vacancy_description(job.link)
        cv_code = ask_openai(job)
        #cover_letter = ask_openai_cover_letter(job, cv_code)
        job.cv_code = cv_code
        #job.cover_letter = cover_letter

        # Send notification to Discord Bot
        try:
            bot_url = os.getenv("BOT_URL")
            requests.post(f"{bot_url}/notify", json=asdict(job))
            print(f"Notification sent for {job.title}")
            save_data(job)
            print(f"Saved {job.title}")
        except Exception as e:
            print(f"Failed to send notification: {e}")
    else:
        print(f"Already exists {job.title}")

delete_old_vacancies(jobs)
