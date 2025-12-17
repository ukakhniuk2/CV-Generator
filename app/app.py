from collector.parser import parse_JustJoinIt, parse_JustJoinIt_vacancy_description
from dataclasses import asdict
import requests
import json
import os
from generator.generator import ask_openai
from database.database import init_db, save_data, data_exists

url = 'https://justjoin.it/job-offers/warszawa/python?experience-level=junior&orderBy=DESC&sortBy=newest'

init_db()

jobs = parse_JustJoinIt(url)

for job in jobs:
    if not data_exists(job.link):
        job.description = parse_JustJoinIt_vacancy_description(job.link)
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
