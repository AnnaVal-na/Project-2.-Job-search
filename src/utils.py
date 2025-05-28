from typing import List
from src.models import Vacancy


def filter_vacancies(
        vacancies: List[Vacancy],
        keywords: List[str]
) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевым словам в описании и названии.

    :param vacancies: Список вакансий для фильтрации
    :param keywords: Список ключевых слов для поиска
    :return: Отфильтрованный список вакансий
    """
    if not keywords:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        description_match = any(
            kw.lower() in vacancy.description.lower()
            for kw in keywords
        )
        title_match = any(
            kw.lower() in vacancy.title.lower()
            for kw in keywords
        )

        if description_match or title_match:
            filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортировка вакансий по убыванию средней зарплаты.

    :param vacancies: Список вакансий для сортировки
    :return: Отсортированный список вакансий
    """

    def get_avg_salary(vacancy: Vacancy) -> int:
        """Вспомогательная функция для расчета средней зарплаты"""
        salary_from = vacancy.salary_from or 0
        salary_to = vacancy.salary_to or 0
        return (salary_from + salary_to) // 2

    return sorted(
        vacancies,
        key=lambda v: get_avg_salary(v),
        reverse=True
    )


def get_top_vacancies(
        vacancies: List[Vacancy],
        n: int
) -> List[Vacancy]:
    """
    Получение топ N вакансий из списка.

    :param vacancies: Исходный список вакансий
    :param n: Количество вакансий для получения
    :return: Список топ N вакансий
    """
    if n <= 0:
        raise ValueError(
            "Количество вакансий должно быть положительным числом"
        )

    return vacancies[:n]
