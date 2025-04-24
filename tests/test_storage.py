import pytest
from src.storage import JSONStorage


@pytest.fixture
def temp_storage(tmp_path):

    return JSONStorage(filename=tmp_path / 'test.json')


def test_add_vacancy(temp_storage):
    vacancy = {'title': 'Test', 'url': 'http://example.com'}
    temp_storage.add_vacancy(vacancy)
    assert len(temp_storage.get_vacancies()) == 1


def test_delete_vacancy(temp_storage):
    vacancy = {'title': 'To Delete', 'url': 'http://example.com'}
    temp_storage.add_vacancy(vacancy)
    temp_storage.delete_vacancy(vacancy)
    assert len(temp_storage.get_vacancies()) == 0


def test_no_duplicates(temp_storage):
    vacancy = {'title': 'Duplicate', 'url': 'http://example.com'}
    temp_storage.add_vacancy(vacancy)
    temp_storage.add_vacancy(vacancy)
    assert len(temp_storage.get_vacancies()) == 1
