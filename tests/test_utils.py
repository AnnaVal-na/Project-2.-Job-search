import pytest
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies
from src.models import Vacancy


def test_filter_vacancies_empty_list(sample_vacancies):
    filtered = filter_vacancies([], ["python"])
    assert filtered == []


def test_sort_vacancies_empty_list():
    sorted_vacs = sort_vacancies([])
    assert sorted_vacs == []


def test_get_top_vacancies_zero_n(sample_vacancies):
    top = get_top_vacancies(sample_vacancies, 0)
    assert len(top) == 0


def test_filter_vacancies_no_keywords(sample_vacancies):
    filtered = filter_vacancies(sample_vacancies, [])
    assert filtered == sample_vacancies


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy('C', 'url3', 150000, 200000, 'JavaScript'),
        Vacancy('A', 'url1', 100000, 150000, 'Python'),
        Vacancy('B', 'url2', 90000, 120000, 'Java')
    ]


def test_filter_vacancies(sample_vacancies):
    filtered = filter_vacancies(sample_vacancies, ['python'])
    assert len(filtered) == 1
    assert filtered[0].title == 'A'


def test_sort_vacancies(sample_vacancies):
    sorted_vacs = sort_vacancies(sample_vacancies)
    assert [v.title for v in sorted_vacs] == ['C', 'A', 'B']


def test_get_top_vacancies(sample_vacancies):
    sorted_vacs = sort_vacancies(sample_vacancies)
    top = get_top_vacancies(sorted_vacs, 2)
    assert len(top) == 2
    assert top[0].title == 'C'
    assert top[1].title == 'A'
