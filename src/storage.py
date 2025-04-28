from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import List, Dict, Optional


class DataStorage(ABC):
    """Абстрактный класс для работы с хранилищами данных"""

    @abstractmethod
    def add_vacancy(self, vacancy: Dict) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict] = None) -> List[Dict]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict) -> None:
        pass


class JSONStorage(DataStorage):
    """Класс для работы с JSON-хранилищем"""

    def __init__(self, filename: str = 'vacancies.json'):
        self.__filename = Path('data') / filename
        self.__filename.parent.mkdir(exist_ok=True)
        self.__filename.touch(exist_ok=True)

    def __read_data(self) -> List[Dict]:
        """Чтение данных из файла"""
        with open(self.__filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def __write_data(self, data: List[Dict]) -> None:
        """Запись данных в файл"""
        with open(self.__filename, 'w') as f:
            json.dump(data, f, indent=2)

    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавление вакансии в файл"""
        data = self.__read_data()
        if vacancy not in data:
            data.append(vacancy)
            self.__write_data(data)

    def get_vacancies(self, criteria: Optional[Dict] = None) -> List[Dict]:
        """Получение вакансий по критериям"""
        data = self.__read_data()
        if criteria:
            # Фильтрация данных по критериям
            filtered_data = []
            for vacancy in data:
                match = True
                for key, value in criteria.items():
                    if vacancy.get(key) != value:
                        match = False
                        break
                if match:
                    filtered_data.append(vacancy)
            return filtered_data
        return data


    def delete_vacancy(self, vacancy: Dict) -> None:
        """Удаление вакансии из файла"""
        data = self.__read_data()
        data = [v for v in data if v != vacancy]
        self.__write_data(data)
