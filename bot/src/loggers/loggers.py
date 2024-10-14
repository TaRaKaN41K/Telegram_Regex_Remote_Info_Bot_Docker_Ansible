import logging

# Общий формат логирования
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Логгер для SSH-команд
ssh_logger = logging.getLogger('ssh_logger')
ssh_logger.setLevel(logging.INFO)
ssh_handler = logging.FileHandler('./logs/paramiko_ssh.log', encoding='utf-8')
ssh_handler.setFormatter(formatter)
ssh_logger.addHandler(ssh_handler)

# Логгер для работы с базой данных
db_logger = logging.getLogger('db_logger')
db_logger.setLevel(logging.INFO)
db_handler = logging.FileHandler('./logs/database.log', encoding='utf-8')
db_handler.setFormatter(formatter)
db_logger.addHandler(db_handler)

# Логгер для Telegram-бота
tg_logger = logging.getLogger('tg_logger')
tg_logger.setLevel(logging.INFO)
tg_handler = logging.FileHandler('./logs/telegram_bot.log', encoding='utf-8')
tg_handler.setFormatter(formatter)
tg_logger.addHandler(tg_handler)
