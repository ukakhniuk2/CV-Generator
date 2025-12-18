import sqlite3
import json
from typing import List, Optional
from collector.models import Vacancy

DB = "database/vacancies.db"

def _conn():
    return sqlite3.connect(DB)

def init_db():
    conn = _conn()
    try:
        with conn as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                link TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                salary TEXT,
                cards TEXT,
                is_remote INTEGER,
                is_one_click INTEGER,
                description TEXT
            )
            """)
    finally:
        conn.close()

def save_data(vac: Vacancy):
    conn = _conn()
    try:
        with conn as c:
            c.execute("""
            INSERT OR IGNORE INTO vacancies
            (link, title, company, location, salary, cards, is_remote, is_one_click, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vac.link,
                vac.title,
                vac.company,
                vac.location,
                vac.salary,
                json.dumps(vac.cards),
                int(vac.is_remote),
                int(vac.is_one_click),
                vac.description
            ))
    finally:
        conn.close()

def data_exists(link: str) -> bool:
    conn = _conn()
    try:
        return conn.execute("SELECT 1 FROM vacancies WHERE link=? LIMIT 1", (link,)).fetchone() is not None
    finally:
        conn.close()

def delete_old_vacancies(jobs: list[Vacancy]):
    if not jobs:
        return

    job_links = {job.link for job in jobs}

    conn = _conn()
    try:
        with conn as c:
            placeholders = ",".join("?" for _ in job_links)
            query = f"""
                DELETE FROM vacancies
                WHERE link NOT IN ({placeholders})
            """
            c.execute(query, tuple(job_links))
    finally:
        conn.close()
