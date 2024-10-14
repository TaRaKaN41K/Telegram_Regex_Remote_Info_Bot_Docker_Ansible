import paramiko
import os
from dotenv import load_dotenv
from loggers.loggers import ssh_logger

load_dotenv()

host = os.getenv('RM_HOST')
port = int(os.getenv('RM_PORT'))
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')


# Функция для выполнения команды на удалённом сервере
def execute_ssh_command(command):
    try:
        # Устанавливаем SSH-соединение
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)
        ssh_logger.info(f"SSH-соединение установлено с {host}")

        # Выполняем команду на сервере
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read().decode('utf-8') or stderr.read().decode('utf-8')

        ssh_logger.info(f"Команда выполнена успешно: {command}")

        # Закрываем соединение
        client.close()
        ssh_logger.info(f"SSH-соединение закрыто с {host}")
        return result
    except Exception as e:
        ssh_logger.error(f"Ошибка при выполнении команды '{command}': {str(e)}")
        return f"Ошибка при выполнении команды: {str(e)}"
