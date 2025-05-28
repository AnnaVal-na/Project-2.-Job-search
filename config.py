import os
from dotenv import load_dotenv

load_dotenv()


DB_NAME = "hh_vacancies"
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('PORT')
