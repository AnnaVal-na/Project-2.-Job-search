import pytest
from src.database import DBManager
from src.models import Employer, Vacancy
from config import DB_NAME, USER, PASSWORD, HOST, PORT
import psycopg2


@pytest.fixture
def test_db():
    # Создаем временную БД для тестов
    conn = psycopg2.connect(
        dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Создаем временную БД
    cur.execute("DROP DATABASE IF EXISTS test_job_search")
    cur.execute("CREATE DATABASE test_job_search")
    cur.close()
    conn.close()

    # Подключаемся к тестовой БД
    test_conn = psycopg2.connect(
        dbname="test_job_search", user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    db_manager = DBManager()
    db_manager.conn = test_conn
    db_manager.create_tables()

    yield db_manager

    # Очистка после тестов
    test_conn.close()
    conn = psycopg2.connect(
        dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("DROP DATABASE test_job_search")
    cur.close()
    conn.close()


def test_get_companies_and_vacancies_count(test_db):
    # Подготовка тестовых данных
    employer1 = Employer(id="1", name="Company A", url="http://a.com", description="")
    employer2 = Employer(id="2", name="Company B", url="http://b.com", description="")

    test_db.insert_employer(employer1)
    test_db.insert_employer(employer2)

    vacancy1 = Vacancy(id="v1", title="Vacancy 1", salary_from=100, salary_to=200,
                       url="http://v1.com", employer_id="1", description="")
    vacancy2 = Vacancy(id="v2", title="Vacancy 2", salary_from=150, salary_to=250,
                       url="http://v2.com", employer_id="1", description="")

    test_db.insert_vacancy(vacancy1)
    test_db.insert_vacancy(vacancy2)

    # Выполнение теста
    result = test_db.get_companies_and_vacancies_count()

    # Проверки
    assert len(result) == 2
    company_counts = {name: count for name, count in result}
    assert company_counts["Company A"] == 2
    assert company_counts["Company B"] == 0


def test_get_all_vacancies(test_db):
    # Подготовка данных
    employer = Employer(id="1", name="Tech Corp", url="http://tech.com", description="")
    test_db.insert_employer(employer)

    vacancy = Vacancy(
        id="v1", title="Python Dev", salary_from=1000, salary_to=2000,
        url="http://vacancy.com", employer_id="1", description=""
    )
    test_db.insert_vacancy(vacancy)

    # Выполнение теста
    result = test_db.get_all_vacancies()

    # Проверки
    assert len(result) == 1
    assert result[0][0] == "Tech Corp"
    assert result[0][1] == "Python Dev"
    assert result[0][4] == "http://vacancy.com"


def test_get_avg_salary(test_db):
    # Подготовка данных
    vacancies = [
        Vacancy(id="v1", title="V1", salary_from=100, salary_to=200, employer_id="1", url="", description=""),
        Vacancy(id="v2", title="V2", salary_from=200, salary_to=300, employer_id="1", url="", description=""),
        Vacancy(id="v3", title="V3", salary_from=0, salary_to=0, employer_id="1", url="", description="")
    ]
    for v in vacancies:
        test_db.insert_vacancy(v)

    # Выполнение теста
    avg_salary = test_db.get_avg_salary()

    # Проверка (100+200)/2 = 150 и (200+300)/2 = 250 => среднее (150+250)/2 = 200
    assert avg_salary == 200.0


def test_get_vacancies_with_higher_salary(test_db):
    # Подготовка данных
    test_db.insert_vacancy(Vacancy(
        id="v1", title="High", salary_from=300, salary_to=400, employer_id="1", url="", description=""
    ))
    test_db.insert_vacancy(Vacancy(
        id="v2", title="Low", salary_from=100, salary_to=200, employer_id="1", url="", description=""
    ))

    # Выполнение теста
    result = test_db.get_vacancies_with_higher_salary()

    # Проверки
    assert len(result) == 1
    assert result[0][1] == "High"


def test_get_vacancies_with_keyword(test_db):
    # Подготовка данных
    vacancies = [
        Vacancy(id="v1", title="Python Developer", salary_from=100, salary_to=200, employer_id="1", url="",
                description=""),
        Vacancy(id="v2", title="Java Engineer", salary_from=150, salary_to=250, employer_id="1", url="",
                description=""),
        Vacancy(id="v3", title="Senior Python", salary_from=200, salary_to=300, employer_id="1", url="", description="")
    ]
    for v in vacancies:
        test_db.insert_vacancy(v)

    # Выполнение теста
    result = test_db.get_vacancies_with_keyword("python")

    # Проверки
    assert len(result) == 2
    titles = {vac[1] for vac in result}
    assert "Python Developer" in titles
    assert "Senior Python" in titles


def test_empty_database_scenarios(test_db):
    # Тестирование пустой БД
    assert test_db.get_companies_and_vacancies_count() == []
    assert test_db.get_all_vacancies() == []
    assert test_db.get_avg_salary() is None
    assert test_db.get_vacancies_with_higher_salary() == []
    assert test_db.get_vacancies_with_keyword("test") == []
