from typing import List
from src.models import Vacancy


def filter_vacancies(
        vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевым словам
    :param vacancies: Список вакансий
    :param keywords: Список ключевых слов
    :return: Отфильтрованный список
    """
    if not keywords:
        return vacancies
    return [v for v in vacancies if any(
        kw.lower() in v.description.lower() for kw in keywords
    )]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по убыванию зарплаты"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """Получение топ N вакансий"""
    return vacancies[:n]
