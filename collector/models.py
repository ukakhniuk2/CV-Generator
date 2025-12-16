from dataclasses import dataclass

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
    description: str | None
