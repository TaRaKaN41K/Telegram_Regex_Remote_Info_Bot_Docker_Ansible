import os
from dotenv import load_dotenv
from telegram.ext import Updater

from telegram_bot.dialog_handlers import *
from loggers.loggers import tg_logger

load_dotenv()

TOKEN = os.getenv('TOKEN')


def main():
    tg_logger.info("Запуск Telegram-бота...")

    try:

        updater = Updater(TOKEN, use_context=True)

        # Получаем диспетчер для регистрации обработчиков
        dp = updater.dispatcher

        tg_logger.info("Telegram-бот успешно запущен.")

        # Регистрируем обработчики команд
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CommandHandler('get_emails', get_emails))
        dp.add_handler(CommandHandler('get_phone_numbers', get_phone_numbers))

        dp.add_handler(conv_handler_find_phone_number)
        dp.add_handler(conv_handler_find_email)
        dp.add_handler(conv_handler_verify_password)

        dp.add_handler(CommandHandler("get_release", get_release))
        dp.add_handler(CommandHandler("get_uname", get_uname))
        dp.add_handler(CommandHandler("get_uptime", get_uptime))
        dp.add_handler(CommandHandler("get_df", get_df))
        dp.add_handler(CommandHandler("get_free", get_free))
        dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
        dp.add_handler(CommandHandler("get_w", get_w))
        dp.add_handler(CommandHandler("get_auths", get_auths))
        dp.add_handler(CommandHandler("get_critical", get_critical))
        dp.add_handler(CommandHandler("get_ps", get_ps))
        dp.add_handler(CommandHandler("get_ss", get_ss))
        dp.add_handler(CommandHandler("get_apt_list", get_apt_list))
        dp.add_handler(CommandHandler("get_services", get_services))
        dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))

        # Запускаем бота
        updater.start_polling()

        tg_logger.info("Telegram-бот начал получать обновления.")

        # Останавливаем бота при нажатии Ctrl+C
        updater.idle()

    except Exception as e:
        tg_logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == '__main__':
    main()
