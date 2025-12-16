import sqlite3
import json
from typing import List, Optional
from collector.models import JustJoinItVacancy

DB = "database/vacancies.db"

def _conn():
    return sqlite3.connect(DB)

def init_db():
    with _conn() as c:
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

def save_data(vac: JustJoinItVacancy):
    with _conn() as c:
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

def data_exists(link: str) -> bool:
    with _conn() as c:
        return c.execute("SELECT 1 FROM vacancies WHERE link=? LIMIT 1", (link,)).fetchone() is not None
