from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Employer:
    id: str
    name: str
    url: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'Employer':
        return cls(
            id=data['id'],
            name=data['name'],
            url=data['alternate_url'],
            description=data.get('description', '')
        )


@dataclass
class Vacancy:
    id: str
    title: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    employer_id: str
    description: str

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List['Vacancy']:
        vacancies = []
        for item in data:
            salary = item.get('salary', {}) or {}
            vacancies.append(cls(
                id=item['id'],
                title=item['name'],
                url=item['alternate_url'],
                salary_from=salary.get('from'),
                salary_to=salary.get('to'),
                employer_id=item['employer']['id'],
                description=item['snippet'].get('requirement', '')
            ))
        return vacancies
