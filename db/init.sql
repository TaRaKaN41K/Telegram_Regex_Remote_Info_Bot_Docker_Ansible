CREATE EXTENSION IF NOT EXISTS dblink;

-- Проверяем, существует ли база данных
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bot_phon_numbers_and_emails_db') THEN
        -- Создаем базу данных, если она не существует
        PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE bot_phon_numbers_and_emails_db');
    END IF;
END
$$;

-- Присваиваем права пользователю на созданную базу данных
GRANT ALL PRIVILEGES ON DATABASE bot_phon_numbers_and_emails_db TO postgres;

-- Переключаемся на базу данных
\c bot_phon_numbers_and_emails_db

-- Создание таблицы emails
CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255)
);

-- Создание таблицы phone_numbers
CREATE TABLE IF NOT EXISTS phone_numbers (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(255)
);

