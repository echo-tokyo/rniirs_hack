import logging
import aiohttp
import json
import sqlite3
import os
import aiosqlite

from config import BASE_DIR

logger = logging.getLogger(__name__)

async def send_to_database(items: list) -> bool:
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
    
async def send_to_database_dev(items: list) -> bool:
    """Временный метод для сохранения новостей в SQLite"""
    db_path = os.path.join(BASE_DIR, "news.sqlite3")
    
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
    

