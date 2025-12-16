from collector.parser import parse_JustJoinIt
from generator.generator import ask_openai

url = 'https://justjoin.it/job-offers/warszawa/python?experience-level=junior&orderBy=DESC&sortBy=newest'

jobs = parse_JustJoinIt(url)

adapted_cv = ask_openai(jobs[0])

print(adapted_cv)
