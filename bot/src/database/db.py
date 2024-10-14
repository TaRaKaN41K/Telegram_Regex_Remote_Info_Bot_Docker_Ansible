import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

from loggers.loggers import db_logger

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_DATABASE')


def create_connection():
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        db_logger.info(f"Подключение к базе данных {database} на {host}:{port} установлено")
        return connection
    except (Exception, Error) as error:
        db_logger.error("Ошибка при подключении к PostgreSQL: %s", error)
