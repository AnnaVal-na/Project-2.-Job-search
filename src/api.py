from abc import ABC, abstractmethod
from typing import Dict, List, Union
import requests


class JobPlatformAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 100) -> List[Dict]:
        pass

    @abstractmethod
    def get_employer(self, employer_id: str) -> Dict:
        pass

    @abstractmethod
    def get_employer_vacancies(self, employer_id: str) -> List[Dict]:
        pass


class HeadHunterAPI(JobPlatformAPI):
    BASE_URL: str = "https://api.hh.ru/vacancies "
    EMPLOYER_URL: str = "https://api.hh.ru/employers "

    def __init__(self) -> None:
        self._headers: Dict[str, str] = {'User-Agent': 'api-test-agent'}
        self._params_template: Dict[str, Union[str, int]] = {
            'text': '',
            'per_page': 100
        }

    def get_vacancies(self, query: str, per_page: int = 100) -> List[Dict]:
        params = self._params_template.copy()
        params.update({'text': query, 'per_page': per_page})
        response = requests.get(
            self.BASE_URL,
            headers=self._headers,
            params=params
        )
        response.raise_for_status()
        return response.json()['items']

    def get_employer(self, employer_id: str) -> Dict:
        url = f"{self.EMPLOYER_URL}/{employer_id}"
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()

    def get_employer_vacancies(self, employer_id: str) -> List[Dict]:
        url = f"{self.BASE_URL}?employer_id={employer_id}"
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()['items']
