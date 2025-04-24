from unittest.mock import Mock, patch
from src.api import HeadHunterAPI


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
            HeadHunterAPI._BASE_URL,
            headers=hh_api._headers,
            params={'text': 'Python', 'per_page': 100}
        )
