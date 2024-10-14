from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram_bot.bot_functions import *
from telegram_bot.bot_command import *

# Обработчик диалога
conv_handler_find_phone_number = ConversationHandler(
    entry_points=[CommandHandler('find_phone_number', find_phone_number_command)],
    states={
        'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)],
        'confirm_phone_numbers': [MessageHandler(Filters.text & ~Filters.command, confirm_phone_numbers)]
    },
    fallbacks=[]
)

conv_handler_find_email = ConversationHandler(
    entry_points=[CommandHandler('find_email', find_email_command)],
    states={
        'find_email': [MessageHandler(Filters.text & ~Filters.command, find_email)],
        'confirm_emails': [MessageHandler(Filters.text & ~Filters.command, confirm_emails)]
    },
    fallbacks=[]
)

conv_handler_verify_password = ConversationHandler(
    entry_points=[CommandHandler('verify_password', verify_password_command)],
    states={
        'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
    },
    fallbacks=[]
)
