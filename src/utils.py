from typing import List
from .models import Vacancy

def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    if not keywords:
        return vacancies
    return [v for v in vacancies if any(kw.lower() in v.description.lower() for kw in keywords)]

def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    return sorted(vacancies, reverse=True)

def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    return vacancies[:n]
