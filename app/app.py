from collector.parser import parse_job_vacancies, parse_job_vacancy_description
from dataclasses import asdict
import requests
import json
import os
from generator.generator import ask_openai
from database.database import init_db, save_data, data_exists, delete_old_vacancies

urls = ['https://justjoin.it/job-offers/warszawa/python?experience-level=junior&orderBy=DESC&sortBy=newest',
        'https://nofluffjobs.com/pl/warszawa/Python?utm_source=google&utm_medium=cpc&utm_campaign=PL_PL_srhbrand1&utm_id=12127570708&gad_source=1&gad_campaignid=12127570708&gbraid=0AAAAADJ4zV3nIRZXNCTw9hmn74kNFwCo2&gclid=Cj0KCQiAxonKBhC1ARIsAIHq_lunm2sFKicAOeCSaPat1mRvKo1NOanykhLwhhC5o58SpJEHOVNwsZAaAhN3EALw_wcB&criteria=jobLanguage%3Dpl,en,ru%20seniority%3Djunior'
]

init_db()

jobs = []
for url in urls:
    jobs.extend(parse_job_vacancies(url))

for job in jobs:
    if not data_exists(job.link):
        job.description = parse_job_vacancy_description(job.link)
        cv_code = ask_openai(job)
        job.cv_code = cv_code
        save_data(job)
        print(f"Saved {job.title}")

        # Send notification to Discord Bot
        try:
            bot_url = os.getenv("BOT_URL")
            requests.post(f"{bot_url}/notify", json=asdict(job))
            print(f"Notification sent for {job.title}")
        except Exception as e:
            print(f"Failed to send notification: {e}")
    else:
        print(f"Already exists {job.title}")

delete_old_vacancies(jobs)
