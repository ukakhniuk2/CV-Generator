from collector.parser import parse_job_vacancies, parse_job_vacancy_description
from dataclasses import asdict
import requests
import os
from generator.generator import ask_openai, ask_openai_cover_letter
from database.database import init_db, save_data, data_exists, delete_old_vacancies
import json
from pathlib import Path

json_path = Path(__file__).parent.parent / "urls.json"
urls = []
if json_path.exists():
    with open(json_path, 'r') as f:
        urls = json.load(f)
else:
    print(f"Warning: {json_path} not found.")

print(f"Tracked urls: {urls}")

init_db()

jobs = []
for url in urls:
    try:
        jobs.extend(parse_job_vacancies(url))
    except Exception as e:
        print(f"Failed to parse vacancies for {url}: {e}")
        continue

for job in jobs:
    if not data_exists(job.link):
        try:
            job.description = parse_job_vacancy_description(job.link)
        except Exception as e:
            print(f"Failed to parse description for {job.title}: {e}")
            continue
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

# delete_old_vacancies(jobs)
