from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Vacancy:
    """Класс для представления вакансии с валидацией данных"""
    __slots__ = (
        '_title', '_url', '_salary_from', '_salary_to', '_description'
    )  # Приватные атрибуты

    def __init__(
            self, title: str,
            url: str,
            salary_from: int,
            salary_to: int,
            description: str
    ):
        self._title = title
        self._url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._description = description
        self.__validate_salary()

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> int:
        return self._salary_from

    @property
    def salary_to(self) -> int:
        return self._salary_to

    @property
    def description(self) -> str:
        return self._description

    def __post_init__(self):
        self.__validate_salary()

    def __validate_salary(self) -> None:
        """Приватный метод валидации данных о зарплате"""
        if self._salary_from < 0 or self._salary_to < 0:
            raise ValueError("Зарплата не может быть отрицательной")

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение вакансий по минимальной зарплате"""
        return self._salary_from < other._salary_from

    def __gt__(self, other: 'Vacancy') -> bool:
        return self._salary_from > other._salary_from

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List['Vacancy']:
        """Преобразование сырых данных в список объектов"""
        vacancies = []
        for item in data:
            salary = item.get('salary', {})
            if salary:
                salary_from = salary.get(
                    'from', 0) if salary.get('from') else 0
                salary_to = salary.get('to', 0) if salary.get('to') else 0
            else:
                salary_from = 0
                salary_to = 0
            vacancies.append(cls(
                title=item['name'],
                url=item['alternate_url'],
                salary_from=salary_from,
                salary_to=salary_to,
                description=item['snippet'].get('requirement', '') or ''
            ))
        return vacancies

    def to_dict(self) -> Dict:
        """Метод для преобразования объекта в словарь"""
        return {
            'title': self._title,
            'url': self._url,
            'salary_from': self._salary_from,
            'salary_to': self._salary_to,
            'description': self._description
        }
