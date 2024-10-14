FROM postgres:14

# Создание директории для конфигурации PostgreSQL
RUN mkdir -p /etc/postgresql/ && \
    mkdir -p /var/log/postgresql/ && \
    chown postgres:postgres /var/log/postgresql/

# Установка прав доступа для каталога данных
RUN chmod 750 /var/lib/postgresql/data

# Установка точки входа
ENTRYPOINT [ "bash", "-c", "\
cat <<EOF > /etc/postgresql/postgresql.conf \n\
listen_addresses = 'localhost, ${DB_REPL_HOST}' \n\
port = ${DB_REPL_PORT} \n\
log_destination = 'stderr' \n\
logging_collector = on \n\
log_directory = '/var/log/postgresql/' \n\
log_filename = 'postgresql-14-main.log' \n\
log_replication_commands = on \n\
EOF\n\
rm -rf /var/lib/postgresql/data/* \n\
sleep 10 \n\
echo ${DB_REPL_PASSWORD} | pg_basebackup -v -R \\\n\
    -h ${DB_HOST} -p ${DB_PORT} -U ${DB_REPL_USER} -W -P \\\n\
    -D /var/lib/postgresql/data \n\
docker-entrypoint.sh $@"]

# Установка команды по умолчанию
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
