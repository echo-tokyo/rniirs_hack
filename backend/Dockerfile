FROM python:3.12.1

SHELL ["/bin/bash", "-c"]

WORKDIR /app/backend


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

# Обновим список пакетов и установим зависимости
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "./entrypoint.sh"]