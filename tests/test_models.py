import pytest
from src.models import Vacancy
from dataclasses import dataclass
from functools import total_ordering
from typing import List, Dict

@total_ordering
@dataclass
class Vacancy:
    """Класс вакансии с поддержкой сравнения"""
    id: str
    title: str
    url: str
    salary_from: int
    salary_to: int
    employer_id: str
    description: str

    def __lt__(self, other: 'Vacancy') -> bool:
        """Сравнение по минимальной зарплате"""
        return self.salary_from < other.salary_from

    def __eq__(self, other: object) -> bool:
        """Проверка равенства вакансий"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from == other.salary_from


def test_to_dict():
    vacancy = Vacancy("Test", "http://example.com", 1000, 2000, "desc")
    expected = {
        "title": "Test",
        "url": "http://example.com",
        "salary_from": 1000,
        "salary_to": 2000,
        "description": "desc"
    }
    assert vacancy.to_dict() == expected

def test_cast_to_object_list_no_salary_key():
    data = [{
        "name": "Test",
        "alternate_url": "url",
        "snippet": {"requirement": ""}
    }]
    vacancies = Vacancy.cast_to_object_list(data)
    assert vacancies[0].salary_from == 0
    assert vacancies[0].salary_to == 0


def test_validate_salary_negative():
    with pytest.raises(ValueError):
        Vacancy("Test", "url", -100, 200, "desc")


def test_vacancy_comparison_edge_cases():
    v1 = Vacancy("A", "url1", 100, 200, "desc")
    v2 = Vacancy("B", "url2", 100, 200, "desc")
    assert not (v1 > v2)
    assert not (v1 < v2)


def test_cast_to_object_list_empty_salary():
    data = [{
        "name": "Test", "alternate_url":
        "url", "salary": None, "snippet": {"requirement": ""}
    }]
    vacancies = Vacancy.cast_to_object_list(data)
    assert vacancies[0].salary_from == 0
    assert vacancies[0].salary_to == 0


def test_vacancy_creation():
    vacancy = Vacancy(
        title='Developer',
        url='http://example.com',
        salary_from=100000,
        salary_to=150000,
        description='Test description'
    )
    assert vacancy.title == 'Developer'
    assert vacancy.salary_from == 100000


def test_salary_validation():
    with pytest.raises(ValueError):
        Vacancy(
            title='Invalid',
            url='http://example.com',
            salary_from=-100,
            salary_to=0,
            description='Test'
        )


def test_vacancy_comparison():
    v1 = Vacancy('A', 'url1', 100000, 150000, 'desc')
    v2 = Vacancy('B', 'url2', 90000, 120000, 'desc')

    assert v1 > v2
    assert v2 < v1


def test_cast_to_object_list():
    test_data = [{
        'name': 'Python Dev',
        'alternate_url': 'http://hh.ru/vacancy/1',
        'salary': {'from': 100000, 'to': 150000},
        'snippet': {'requirement': 'Python experience'}
    }]

    vacancies = Vacancy.cast_to_object_list(test_data)
    assert len(vacancies) == 1
    assert vacancies[0].title == 'Python Dev'

@dataclass
class Employer:
    id: str
    name: str
    url: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'Employer':
        return cls(
            id=data['id'],
            name=data['name'],
            url=data['alternate_url'],
            description=data.get('description', '')
        )
