import psycopg2
from config import DB_NAME, USER, PASSWORD, HOST, PORT
from typing import List
from src.models import Employer, Vacancy


class DBManager:
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        self.conn.autocommit = True

    def create_tables(self) -> None:
        """Создание таблиц employers и vacancies"""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    url VARCHAR(100),
                    description TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id VARCHAR(20) PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url VARCHAR(100),
                    employer_id VARCHAR(20) REFERENCES employers(id),
                    description TEXT
                )
            """)

    def insert_employer(self, employer: Employer) -> None:
        """Добавление работодателя в БД"""
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO employers (id, name, url, description)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (employer.id, employer.name, employer.url, employer.description)
            )

    def insert_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в БД"""
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO vacancies 
                   (id, title, salary_from, salary_to, url, employer_id, description)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (vacancy.id, vacancy.title, vacancy.salary_from,
                 vacancy.salary_to, vacancy.url, vacancy.employer_id, vacancy.description)
            )

    def get_companies_and_vacancies_count(self) -> List[tuple]:
        """Получение списка компаний и количества вакансий"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.id)
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[tuple]:
        """Получение списка всех вакансий"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Вычисление средней зарплаты"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2)
                FROM vacancies
            """)
            result = cur.fetchone()[0]
            return float(result) if result is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """Получение вакансий с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE ((COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2) > %s
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """Поиск вакансий по ключевому слову"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.title ILIKE %s
            """, (f"%{keyword}%",))
            return cur.fetchall()
