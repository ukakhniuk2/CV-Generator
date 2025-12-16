from collector.parser import parse_JustJoinIt
from generator.generator import ask_openai
from database.database import init_db, save, exists

url = 'https://justjoin.it/job-offers/warszawa/python?experience-level=junior&orderBy=DESC&sortBy=newest'

init_db()
