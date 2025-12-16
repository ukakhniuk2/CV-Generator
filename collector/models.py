from dataclasses import dataclass

HEADER_ID = "01"
TRANSACTION_ID = "02"
FOOTER_ID = "03"

@dataclass
class JustJoinItVacancy:
    link: str
    title: str
    company: str
    location: str
    salary: str
    cards: list
    is_remote: bool
    is_one_click: bool
