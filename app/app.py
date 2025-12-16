from collector.parser import parse_JustJoinIt

url = 'https://justjoin.it/job-offers/warszawa/python?experience-level=junior&orderBy=DESC&sortBy=newest'

jobs = parse_JustJoinIt(url)
print(jobs)
