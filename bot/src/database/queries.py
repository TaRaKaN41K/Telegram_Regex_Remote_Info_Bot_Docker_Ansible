from database.db import create_connection, db_logger


def fetch_emails():
    connection = None
    cursor = None
    data = []
    try:
        db_logger.info("Запрос email-адресов из базы данных.")

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()

        db_logger.info(f"Успешно получены {len(data)} email-адресов.")

    except Exception as e:
        db_logger.error(f"Ошибка при выполнении SELECT email-адресов: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
    return data


def fetch_phone_numbers():
    connection = None
    cursor = None
    data = []
    try:
        db_logger.info("Запрос номеров телефонов из базы данных.")

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phone_numbers;")
        data = cursor.fetchall()

        db_logger.info(f"Успешно получены {len(data)} номеров телефонов.")

    except Exception as e:
        db_logger.error(f"Ошибка при выполнении SELECT номеров телефонов: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
    return data


def insert_emails(emails_list):
    connection = None
    cursor = None
    try:
        db_logger.info("Запрос на добавление email-адресов в базу данных.")

        connection = create_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO emails (email) VALUES (%s)"

        for email in emails_list:
            cursor.execute(insert_query, (email,))
        connection.commit()

        db_logger.info(f"Успешно добавлено {len(emails_list)} email-адресов.")

        return True
    except Exception as e:
        db_logger.error(f"Ошибка при записи email-адресов: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def insert_phone_numbers(phone_numbers_list):
    connection = None
    cursor = None
    try:
        db_logger.info("Запрос на добавление номеров телефонов в базу данных.")

        connection = create_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO phone_numbers (phone_number) VALUES (%s)"
        for number in phone_numbers_list:
            cursor.execute(insert_query, (number,))
        connection.commit()

        db_logger.info(f"Успешно получены {len(phone_numbers_list)} номеров телефонов.")

        return True
    except Exception as e:
        db_logger.error(f"Ошибка при записи номеров телефонов: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
