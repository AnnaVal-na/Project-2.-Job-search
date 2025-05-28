from src.database import DBManager
from src.api import HeadHunterAPI
from src.models import Employer, Vacancy

def initialize_database():
    """Инициализация базы данных"""
    db = DBManager()
    db.create_tables()
    return db

def load_data_to_db(db: DBManager):
    """Загрузка данных в базу"""
    hh_api = HeadHunterAPI()
    company_ids = [
        '15478', '1740', '78638', '908583', '1455', '1122462', '4934', '641093', '358288', '10506'
    ]
    for company_id in company_ids:
        employer_data = hh_api.get_employer(company_id)
        employer = Employer.from_dict(employer_data)
        db.insert_employer(employer)
        vacancies_data = hh_api.get_employer_vacancies(company_id)
        for vacancy in Vacancy.cast_to_object_list(vacancies_data):
            db.insert_vacancy(vacancy)

def user_interaction():
    """Функция взаимодействия с пользователем"""
    db = DBManager()
    while True:
        print("\n--- Меню ---")
        print("1. Компании и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            for name, count in db.get_companies_and_vacancies_count():
                print(f"{name}: {count} вакансий")
        elif choice == '2':
            for vac in db.get_all_vacancies():
                print(f"{vac[0]} - {vac[1]}: {vac[2]}-{vac[3]} {vac[4]}")
        elif choice == '3':
            print(f"Средняя зарплата: {db.get_avg_salary():.2f}")
        elif choice == '4':
            for vac in db.get_vacancies_with_higher_salary():
                print(f"{vac[0]} - {vac[1]}: {vac[2]}-{vac[3]} {vac[4]}")
        elif choice == '5':
            keyword = input("Введите ключевое слово: ")
            for vac in db.get_vacancies_with_keyword(keyword):
                print(f"{vac[0]} - {vac[1]}: {vac[2]}-{vac[3]} {vac[4]}")
        elif choice == '0':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    db = initialize_database()
    # Закомментировано для тестирования
    # load_data_to_db(db)
    user_interaction()
