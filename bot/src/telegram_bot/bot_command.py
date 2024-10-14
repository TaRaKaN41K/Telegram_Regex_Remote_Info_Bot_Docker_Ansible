from telegram import Update
from loggers.loggers import tg_logger


def start(update: Update, context):
    user = update.effective_user
    tg_logger.info(f'Пользователь {user.full_name} ( @{user.username} ) запустил бота.')
    update.message.reply_text(f'Привет {user.full_name}!')


def help_command(update, context):
    user = update.effective_user
    help_text = (
        "📧 **Поиск информации**:\n"
        "/find_email - Найти все email-адреса в предоставленном тексте.\n"
        "/get_emails - Вся информация по найденым email-адресам (вся бд)\n"
        "/find_phone_number - Найти все номера телефонов в предоставленном тексте.\n"
        "/get_phone_numbers - Вся информация по найденым номерам (вся бд)\n"
        "/verify_password - Проверить сложность пароля.\n\n"
        "🖥 **Мониторинг системы**:\n"
        "/get_release - Информация о релизе системы.\n"
        "/get_uname - Архитектура процессора, имя хоста и версия ядра.\n"
        "/get_uptime - Время работы системы.\n"
        "/get_df - Состояние файловой системы.\n"
        "/get_free - Состояние оперативной памяти.\n"
        "/get_mpstat - Информация о производительности системы.\n"
        "/get_w - Список активных пользователей.\n"
        "/get_auths - Последние 10 входов в систему.\n"
        "/get_critical - Последние 5 критических событий.\n"
        "/get_ps - Список запущенных процессов.\n"
        "/get_ss - Информация об используемых портах.\n"
        "/get_apt_list <package name> - Информация об установленных пакетах. Если не указано имя пакета, выводится информация о всех.\n"
        "/get_services - Список запущенных сервисов.\n"
        "/get_repl_logs - Получение 20 последни строк логов репликации\n\n"
        "ℹ️ **Как это работает**:\n"
        "1. Введите команду.\n"
        "2. Следуйте указаниям бота для выполнения задачи.\n\n"
        "Для любой команды, если данные не найдены, бот сообщит об этом."
    ).replace('_', r'\_')  # Экранирование символов подчеркивания

    tg_logger.info(f"Пользователь {user.full_name} ( @{user.username} ) запрашивает помощь.")
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode='Markdown')


def find_phone_number_command(update: Update, context):
    user = update.effective_user
    tg_logger.info(f"Пользователь {user.full_name} ( @{user.username} ) запрашивает поиск телефонных номеров.")
    update.message.reply_text('Введите текст для поиска телефонных номеров')

    return 'find_phone_number'


def find_email_command(update: Update, context):
    user = update.effective_user
    tg_logger.info(f"Пользователь {user.full_name} ( @{user.username} ) запрашивает поиск email-адресов.")
    update.message.reply_text('Введите текст для поиска email')

    return 'find_email'


def verify_password_command(update: Update, context):
    user = update.effective_user
    tg_logger.info(f"Пользователь {user.full_name} ( @{user.username} ) запрашивает проверку пароля.")
    update.message.reply_text('Пожалуйста, отправьте пароль для проверки его сложности')

    return 'verify_password'
