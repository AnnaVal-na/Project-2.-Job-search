import pytest
from src.models import Vacancy


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
