# Используем Python 3.11
FROM python:3.12.1

SHELL ["/bin/sh", "-c"]

# Устанавливаем cron
RUN apt-get update && apt-get install -y cron

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем файл с задачей для cron
RUN echo "*/2 * * * * /usr/local/bin/python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/parser-cron

# Даем права на выполнение cron файла
RUN chmod 0644 /etc/cron.d/parser-cron

# Применяем crontab
RUN crontab /etc/cron.d/parser-cron

# Создаем лог файл и даем права на запись
RUN touch /var/log/cron.log && chmod 0666 /var/log/cron.log

# Копируем весь код парсера
COPY . .

# Используем JSON формат для CMD
ENTRYPOINT ["sh", "./start.sh"]
