from abc import ABC, abstractmethod
from typing import Dict, List
import requests


class JobPlatformAPI(ABC):
    """Абстрактный класс для работы с API платформ вакансий"""

    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 100) -> List[Dict]:
        pass


class HeadHunterAPI(JobPlatformAPI):
    """Класс для работы с API HeadHunter"""

    BASE_URL = "https://api.hh.ru/vacancies"  # Делаем атрибут публичным

    def __init__(self):
        self._headers = {'User-Agent': 'api-test-agent'}
        self._params_template = {'text': '', 'per_page': 100}

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
