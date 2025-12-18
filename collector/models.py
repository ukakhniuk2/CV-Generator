from dataclasses import dataclass

@dataclass
class Vacancy:
    link: str
    title: str
    company: str
    location: str
    salary: str
    cards: list
    is_remote: bool
    is_one_click: bool
    description: str | None
    cv_code: str | None
    cover_letter: str | None
