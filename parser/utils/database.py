import logging
import aiohttp
import json
import sqlite3
import os
import aiosqlite
import csv
from datetime import datetime

from config import BASE_DIR

logger = logging.getLogger(__name__)

async def send_to_database_prod(items: list) -> bool:
    """Отправляет новости в базу данных через API"""
    logger.info(f"[{items[0].get('author', 'Unknown')}] Отправка пакета из {len(items)} новостей")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://djangoapp:8000/api-dev/news/',
                json=items,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 201:  # Успешное создание
                    logger.info(f"Успешно отправлено {len(items)} новостей")
                    return True
                else:
                    logger.error(f"Ошибка при отправке новостей: {response.status}")
                    error_text = await response.text()
                    logger.error(f"Ответ сервера: {error_text}")
                    return False
                    
    except Exception as e:
        logger.error(f"Ошибка при отправке данных в БД: {str(e)}")
        return False
    
async def send_to_database(items: list) -> bool:
    """Временный метод для сохранения новостей в SQLite"""
    db_path = os.path.join(BASE_DIR, "rscf_news.sqlite3")
    
    # Убедимся, что директория существует
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        async with aiosqlite.connect(db_path) as db:
            # Создаем таблицу, если она не существует
            await db.execute('''
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    author TEXT,
                    category TEXT,
                    link TEXT UNIQUE,
                    date TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Подготавливаем данные для вставки
            for item in items:
                try:
                    await db.execute('''
                        INSERT INTO news (title, description, author, category, link, date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        item.get('title', ''),
                        item.get('description', ''),
                        item.get('author', ''),
                        item.get('category', ''),
                        item.get('link', ''),
                        item.get('date', '')
                    ))
                except sqlite3.IntegrityError:
                    # Пропускаем дубликаты (если link уже существует)
                    logger.debug(f"Новость уже существует: {item.get('title')}")
                    continue
                except Exception as e:
                    logger.error(f"Ошибка при сохранении новости: {str(e)}")
                    continue
            
            await db.commit()
            logger.info(f"Сохранено {len(items)} новостей в SQLite")
            return True
            
    except Exception as e:
        logger.error(f"Ошибка при работе с SQLite: {str(e)}")
        return False
    
async def save_to_csv(items: list) -> bool:
    """Сохраняет новости в CSV файл для анализа"""
    csv_path = os.path.join(BASE_DIR, "news_dataset.csv")
    
    try:
        # Создаем директорию, если её нет
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Определяем режим открытия файла (append или write)
        file_mode = 'a' if os.path.exists(csv_path) else 'w'
        write_header = not os.path.exists(csv_path)
        
        with open(csv_path, mode=file_mode, encoding='utf-8', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            
            # Записываем заголовок только если файл новый
            if write_header:
                writer.writerow(['text', 'label'])
            
            # Записываем данные
            for item in items:
                # Записываем только заголовок и категорию
                title = item.get('title', '').strip()
                category = item.get('category', 'Новости Фонда')
                
                if title:  # Проверяем, что заголовок не пустой
                    writer.writerow([title, category])
                
                # Если нужно также сохранять полный текст новости
                # description = item.get('description', '').strip()
                # if description:  # Проверяем, что описание не пустое
                #     writer.writerow([description, category])
        
        logger.info(f"Данные успешно сохранены в CSV: {csv_path}")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении в CSV: {str(e)}")
        return False

# Функция для создания датасета из существующей БД SQLite
async def create_dataset_from_db() -> bool:
    """Создает CSV датасет из существующей базы данных SQLite"""
    db_path = os.path.join(BASE_DIR, "rscf_news.sqlite3")
    csv_path = os.path.join(BASE_DIR, "news_dataset.csv")
    
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute('''
                SELECT title, description, category 
                FROM news 
                WHERE category IS NOT NULL
            ''') as cursor:
                rows = await cursor.fetchall()
                
                with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                    writer.writerow(['text', 'label'])
                    
                    for row in rows:
                        # Записываем заголовок
                        if row[0]:  # title
                            writer.writerow([row[0].strip(), row[2]])  # title, category
                        
                        # Записываем описание
                        if row[1]:  # description
                            writer.writerow([row[1].strip(), row[2]])  # description, category
                
                logger.info(f"Датасет успешно создан: {csv_path}")
                logger.info(f"Всего записей обработано: {len(rows)}")
                return True
                
    except Exception as e:
        logger.error(f"Ошибка при создании датасета: {str(e)}")
        return False
    

