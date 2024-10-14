import re
from telegram import Update
from telegram.ext import ConversationHandler

from paramiko_client.paramiko_client import execute_ssh_command
from loggers.loggers import tg_logger
from database.queries import *


def find_phone_number(update: Update, context):
    user_input = update.message.text
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) запрашивает поиск телефонных номеров.")
    phone_num_regex = re.compile(r'(?:[1-9]\d{9}|\d{3}-\d{2}-\d{2}|(?:\+7|7|8)\s*[-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})')

    phone_number_list = phone_num_regex.findall(user_input)

    if not phone_number_list:
        tg_logger.info(f"Телефонные номера не найдены для пользователя {update.effective_user.full_name} ( @{update.effective_user.username} ) .")
        update.message.reply_text('Телефонные номера не найдены')
        update.message.reply_text('Введите текст для поиска телефонных номеров: ')
        return

    phone_numbers = ''
    for i in range(len(phone_number_list)):
        phone_numbers += f'{i + 1}. {phone_number_list[i]}\n'

    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Найденные номера телефонов: {' | '.join(phone_number_list)}")
    update.message.reply_text(phone_numbers)
    update.message.reply_text('Вы хотите сохранить найденные номера в базу данных? (да/нет)')
    context.user_data['phone_numbers'] = phone_number_list
    return 'confirm_phone_numbers'


def find_email(update: Update, context):
    user_input = update.message.text
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) запрашивает поиск email-адресов.")

    emails_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    emails_list = emails_regex.findall(user_input)

    if not emails_list:
        tg_logger.info(f"Email не найдены для пользователя {update.effective_user.full_name} ( @{update.effective_user.username} ) .")
        update.message.reply_text('Email не найдены')
        update.message.reply_text('Введите текст для поиска email: ')
        return

    emails = ''
    for i in range(len(emails_list)):
        emails += f'{i + 1}. {emails_list[i]}\n'

    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Найденные email-адреса: {' | '.join(emails_list)}")
    update.message.reply_text(emails)
    update.message.reply_text('Вы хотите сохранить найденные email-адреса в базу данных? (да/нет)')
    context.user_data['emails'] = emails_list
    return 'confirm_emails'


def confirm_phone_numbers(update: Update, context):
    response = update.message.text.lower()
    if response == 'да':
        phone_numbers = context.user_data.get('phone_numbers', [])
        tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username}) подтвердил сохранение номеров телефонов: {' | '.join(phone_numbers)}")
        if phone_numbers:
            success = insert_phone_numbers(phone_numbers)
            if success:
                update.message.reply_text('Номера телефонов успешно записаны в базу данных.')
                tg_logger.info(f"Номера телефонов {' '.join(phone_numbers)} успешно записаны в базу данных пользователем {update.effective_user.full_name} ( @{update.effective_user.username})")
            else:
                update.message.reply_text('Произошла ошибка при записи номеров телефонов в базу данных.')
                tg_logger.error(f"Ошибка при записи номеров телефонов {' '.join(phone_numbers)} для пользователя {update.effective_user.full_name} ( @{update.effective_user.username})")
        return ConversationHandler.END
    else:
        update.message.reply_text('Запись номеров телефонов отменена.')
        tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username}) отменил запись номеров телефонов.")
        return ConversationHandler.END


def confirm_emails(update: Update, context):
    response = update.message.text.lower()
    if response == 'да':
        emails = context.user_data.get('emails', [])
        tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username}) подтвердил сохранение email-адресов: {' | '.join(emails)}")
        if emails:
            success = insert_emails(emails)
            if success:
                update.message.reply_text('Email-адреса успешно записаны в базу данных.')
                tg_logger.info(f"Email-адреса {' '.join(emails)} успешно записаны в базу данных пользователем {update.effective_user.full_name} ( @{update.effective_user.username})")
            else:
                update.message.reply_text('Произошла ошибка при записи email-адресов в базу данных.')
                tg_logger.error(f"Ошибка при записи email-адресов {' '.join(emails)} для пользователя {update.effective_user.full_name} ( @{update.effective_user.username})")
        return ConversationHandler.END
    else:
        update.message.reply_text('Запись email-адресов отменена.')
        tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username}) отменил запись email-адресов.")
        return ConversationHandler.END


def verify_password(update: Update, context):
    password = update.message.text
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) запрашивает проверку пароля.")
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

    # Проверяем пароль с использованием регулярного выражения
    if password_regex.match(password):
        tg_logger.info(f"Пароль сложный для пользователя {update.effective_user.full_name} ( @{update.effective_user.username} ) .")
        update.message.reply_text('Пароль сложный.')
    else:
        tg_logger.info(f"Пароль простой для пользователя {update.effective_user.full_name} ( @{update.effective_user.username} ) .")
        update.message.reply_text('Пароль простой. Пароль должен содержать:\n'
                                  '- Не менее 8 символов\n'
                                  '- Как минимум одну заглавную букву\n'
                                  '- Как минимум одну строчную букву\n'
                                  '- Как минимум одну цифру\n'
                                  '- Как минимум один специальный символ (@$!%*?&)')

    return ConversationHandler.END


# Команда для получения релиза системы
def get_release(update: Update, context):
    result = execute_ssh_command('cat /etc/*release')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение информации о релизе системы.")
    update.message.reply_text(result)


# Команда для получения информации о процессоре, хосте и версии ядра
def get_uname(update: Update, context):
    result = execute_ssh_command('uname -a')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение информации о процессоре и системе.")
    update.message.reply_text(result)


# Команда для получения времени работы системы
def get_uptime(update: Update, context):
    result = execute_ssh_command('uptime')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение времени работы системы.")
    update.message.reply_text(result)


# Команда для получения состояния файловой системы
def get_df(update: Update, context):
    result = execute_ssh_command('df -h')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение состояния файловой системы.")
    update.message.reply_text(result)


# Команда для получения информации о состоянии оперативной памяти
def get_free(update: Update, context):
    result = execute_ssh_command('free -h')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение информации о состоянии оперативной памяти.")
    update.message.reply_text(result)


# Команда для получения информации о производительности системы
def get_mpstat(update: Update, context):
    result = execute_ssh_command('mpstat')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение информации о производительности системы.")
    update.message.reply_text(result)


# Команда для получения списка работающих пользователей
def get_w(update: Update, context):
    result = execute_ssh_command('w')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение списка активных пользователей.")
    update.message.reply_text(result)


# Команда для получения последних 10 входов в систему
def get_auths(update: Update, context):
    result = execute_ssh_command('last -n 10')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение последних 10 входов в систему.")
    update.message.reply_text(result)


# Команда для получения последних 5 критических событий
def get_critical(update: Update, context):
    result = execute_ssh_command('grep -i "critical" /var/log/syslog | tail -n 5')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение последних 5 критических событий.")
    update.message.reply_text(result)


# Команда для получения списка запущенных процессов
def get_ps(update: Update, context):
    try:
        # Выполняем команду для получения списка процессов
        result = execute_ssh_command('ps aux')
        tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение списка запущенных процессов.")

        # Проверяем длину результата и разбиваем на части, если он слишком длинный
        max_message_length = 4096
        if len(result) > max_message_length:
            for i in range(0, len(result), max_message_length):
                context.bot.send_message(chat_id=update.effective_chat.id, text=result[i:i + max_message_length])
        else:
            update.message.reply_text(result)

    except Exception as e:
        # Обработка ошибок и отправка сообщения пользователю
        tg_logger.error(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Ошибка при выполнении команды ps: {str(e)}")
        update.message.reply_text(f'Ошибка при выполнении команды: {str(e)}')


# Команда для получения информации об используемых портах
def get_ss(update: Update, context):
    result = execute_ssh_command('ss -tuln')
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Получение информации об используемых портах.")
    update.message.reply_text(result)


# Команда для получения списка установленных пакетов
def get_apt_list(update: Update, context):
    try:
        user = update.effective_user
        if context.args:
            # Поиск информации о конкретном пакете
            package = context.args[0]
            tg_logger.info(f"Пользователь {user.full_name} ( @{user.username} ) запрашивает информацию о пакете {package}.")
            result = execute_ssh_command(f'apt list --installed {package}')
            if result:
                update.message.reply_text(result)
                tg_logger.info(f"Пакет {package} найден и информация отправлена пользователю {user.full_name} ( @{user.username} ).")
            else:
                update.message.reply_text(f'Пакет "{package}" не найден.')
                tg_logger.info(f"Пакет {package} не найден для пользователя {user.full_name} ( @{user.username} ).")
        else:
            tg_logger.info(f"Пользователь {user.full_name} ( @{user.username} ) запрашивает список всех установленных пакетов.")
            # Вывод всех установленных пакетов
            result = execute_ssh_command('apt list --installed')

            # Проверяем длину результата и разбиваем на части, если он слишком длинный
            max_message_length = 4096
            if len(result) > max_message_length:
                for i in range(0, len(result), max_message_length):
                    context.bot.send_message(chat_id=update.effective_chat.id, text=result[i:i + max_message_length])
            else:
                update.message.reply_text(result)
            tg_logger.info(f"Список установленных пакетов отправлен пользователю {user.full_name}  ( @{user.username} ).")


    except Exception as e:
        # Обработка ошибок и отправка сообщения пользователю
        tg_logger.error(f"Ошибка при выполнении команды apt list для пользователя {user.full_name}  ( @{user.username} ) : {str(e)}")
        update.message.reply_text(f'Ошибка при выполнении команды: {str(e)}')


# Команда для получения списка запущенных сервисов
def get_services(update: Update, context):
    try:
        user = update.effective_user
        tg_logger.info(f"Пользователь {user.full_name}  ( @{user.username} ) запрашивает список запущенных сервисов.")
        result = execute_ssh_command('systemctl list-units --type=service --state=running')

        # Проверяем длину результата и разбиваем на части, если он слишком длинный
        max_message_length = 4096
        if len(result) > max_message_length:
            for i in range(0, len(result), max_message_length):
                context.bot.send_message(chat_id=update.effective_chat.id, text=result[i:i + max_message_length])
        else:
            update.message.reply_text(result)
        tg_logger.info(f"Список запущенных сервисов отправлен пользователю {user.full_name}  ( @{user.username} ) .")

    except Exception as e:
        # Обработка ошибок и отправка сообщения пользователю
        tg_logger.error(f"Ошибка при выполнении команды systemctl для пользователя {user.full_name} ( @{user.username} ) : {str(e)}")
        update.message.reply_text(f'Ошибка при выполнении команды: {str(e)}')


def get_repl_logs(update: Update, context):
    try:
        user = update.effective_user
        tg_logger.info(f"Пользователь {user.full_name}  ( @{user.username} ) запрашивает последние 20 строк логов репликации.")
        # Выполняем команду для получения 20 последних строк логов репликации
        result = execute_ssh_command('tail -n 20 /var/log/postgresql/postgresql-14-main.log')

        # Проверяем длину результата и разбиваем на части, если он слишком длинный
        max_message_length = 4096
        if len(result) > max_message_length:
            for i in range(0, len(result), max_message_length):
                context.bot.send_message(chat_id=update.effective_chat.id, text=result[i:i + max_message_length])
        else:
            update.message.reply_text(result)
        tg_logger.info(f"Логи репликации отправлены пользователю {user.full_name}  ( @{user.username} ) .")

    except Exception as e:
        # Обработка ошибок и отправка сообщения пользователю
        tg_logger.error(
            f"Ошибка при выполнении команды для получения логов репликации для пользователя {user.full_name}  ( @{user.username} ) : {str(e)}")
        update.message.reply_text(f'Ошибка при выполнении команды: {str(e)}')


def get_emails(update: Update, context):
    result = fetch_emails()
    formatted_result = '\n'.join([f"{email[0]}. {email[1]}" for email in result])
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Запрос базы данных emails")
    update.message.reply_text(formatted_result)


def get_phone_numbers(update: Update, context):
    result = fetch_phone_numbers()
    formatted_result = '\n'.join([f"{phone_number[0]}. {phone_number[1]}" for phone_number in result])
    tg_logger.info(f"Пользователь {update.effective_user.full_name} ( @{update.effective_user.username} ) : Запрос базы данных phone_numbers")
    update.message.reply_text(formatted_result)
