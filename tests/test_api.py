from unittest.mock import patch, Mock
import pytest
import requests
from src.api import HeadHunterAPI


def test_get_vacancies_with_criteria():
    # Тест для проверки получения вакансий по критериям
    # Убедитесь, что этот тест не зависит от temp_storage
    pass


def test_read_data_empty_file(temp_storage):
    # Тест для проверки чтения пустого файла
    assert temp_storage.get_vacancies() == []

def test_get_vacancies_with_criteria(temp_storage):
    temp_storage.add_vacancy({"title": "Python Dev", "url": "http://example.com"})
    temp_storage.add_vacancy({"title": "Java Dev", "url": "http://example.com"})
    result = temp_storage.get_vacancies(criteria={"title": "Python Dev"})
    assert len(result) == 1
    assert result[0]["title"] == "Python Dev"

def test_read_data_empty_file(temp_storage):
    assert temp_storage.get_vacancies() == []


def test_get_vacancies_invalid_params():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response
        hh_api = HeadHunterAPI()
        result = hh_api.get_vacancies(None)  # Передаем None как некорректный параметр
        assert len(result) == 0


def test_get_vacancies_network_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException("Network error")
        hh_api = HeadHunterAPI()
        with pytest.raises(requests.RequestException):
            hh_api.get_vacancies("Python")


def test_get_vacancies_empty_response():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response
        hh_api = HeadHunterAPI()
        result = hh_api.get_vacancies("Python")
        assert len(result) == 0


def test_get_vacancies():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'id': '1'}]}
        mock_get.return_value = mock_response
        hh_api = HeadHunterAPI()
        result = hh_api.get_vacancies('Python')
        assert len(result) == 1
        assert result[0]['id'] == '1'
        mock_get.assert_called_once_with(
            HeadHunterAPI.BASE_URL,
            headers=hh_api._headers,
            params={'text': 'Python', 'per_page': 100}
        )
