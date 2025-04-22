from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import List, Dict


class DataStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Dict) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict = None) -> List[Dict]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict) -> None:
        pass


class JSONStorage(DataStorage):
    def __init__(self, filename: str = 'vacancies.json'):
        self.__filename = Path('data') / filename
        self.__filename.parent.mkdir(exist_ok=True)
        self.__filename.touch(exist_ok=True)

    def __read_data(self) -> List[Dict]:
        with open(self.__filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def __write_data(self, data: List[Dict]) -> None:
        with open(self.__filename, 'w') as f:
            json.dump(data, f, indent=2)

    def add_vacancy(self, vacancy: Dict) -> None:
        data = self.__read_data()
        if vacancy not in data:
            data.append(vacancy)
            self.__write_data(data)

    def get_vacancies(self, criteria: Dict = None) -> List[Dict]:
        data = self.__read_data()
        # Implement filtering logic
        return data

    def delete_vacancy(self, vacancy: Dict) -> None:
        data = self.__read_data()
        data = [v for v in data if v != vacancy]
        self.__write_data(data)
        