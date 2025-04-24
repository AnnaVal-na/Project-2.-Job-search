from src.api import HeadHunterAPI
from src.models import Vacancy
from src.storage import JSONStorage
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    query = input("Введите поисковый запрос: ")
    vacancies = hh_api.get_vacancies(query)
    vacancy_objects = Vacancy.cast_to_object_list(vacancies)

    # Сохранение результатов
    for vac in vacancy_objects:
        storage.add_vacancy(vac.__dict__)

    # Фильтрация и сортировка
    top_n = int(input("Введите количество вакансий для вывода: "))
    keywords = input("Введите ключевые слова через пробел: ").split()

    filtered = filter_vacancies(vacancy_objects, keywords)
    sorted_vacs = sort_vacancies(filtered)
    top_vacs = get_top_vacancies(sorted_vacs, top_n)

    # Вывод результатов
    for idx, vac in enumerate(top_vacs, 1):
        print(f"""
        {idx}. {vac.title}
        Зарплата: {vac.salary_from} - {vac.salary_to}
        Описание: {vac.description}
        Ссылка: {vac.url}
        {'-' * 50}
        """)


if __name__ == "__main__":
    user_interaction()
