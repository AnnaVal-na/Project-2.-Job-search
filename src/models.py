from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Vacancy:
    """Класс для представления вакансии с валидацией данных"""

    __slots__ = ('title', 'url', 'salary_from', 'salary_to', 'description')
    title: str
    url: str
    salary_from: int
    salary_to: int
    description: str

    def __post_init__(self):
        self.__validate_salary()

    def __validate_salary(self) -> None:
        """Приватный метод валидации данных о зарплате"""
        if self.salary_from < 0 or self.salary_to < 0:
            raise ValueError("Зарплата не может быть отрицательной")

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по минимальной зарплате"""
        return self.salary_from < other.salary_from

    def __gt__(self, other: 'Vacancy') -> bool:
        return self.salary_from > other.salary_from

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List['Vacancy']:
        """Преобразование сырых данных в список объектов"""
        vacancies = []
        for item in data:
            salary = item.get('salary', {})
            vacancies.append(cls(
                title=item['name'],
                url=item['alternate_url'],
                salary_from=salary.get('from', 0) if salary else 0,
                salary_to=salary.get('to', 0) if salary else 0,
                description=item['snippet'].get('requirement', '') or ''
            ))
        return vacancies
