import requests
from abc import ABC, abstractmethod
from typing import Dict, List


class JobPlatformAPI(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 100) -> List[Dict]:
        pass


class HeadHunterAPI(JobPlatformAPI):
    __BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.__headers = {'User-Agent': 'api-test-agent'}
        self.__params = {'text': '', 'per_page': 100}

    def connect(self) -> None:
        response = requests.get(self.__BASE_URL, headers=self.__headers)
        response.raise_for_status()

    def get_vacancies(self, query: str, per_page: int = 100) -> List[Dict]:
        self.__params.update({'text': query, 'per_page': per_page})
        self.connect()
        response = requests.get(self.__BASE_URL, params=self.__params, headers=self.__headers)
        return response.json()['items']
    