import json
import os
import logging
from typing import Set
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)

def get_unique_categories() -> Set[str]:
    """Получает все уникальные категории из сохраненных новостей"""
    json_file = os.path.join(BASE_DIR, "news_example.json")
    categories = set()
    
    try:
        with open(os.path.join(BASE_DIR, "..", "news_example.json"), 'r', encoding='utf-8') as f:
            news_items = json.load(f)
            for news in news_items:
                categories.add(news['category'])
        
        logger.info(f"Найдено {len(categories)} уникальных категорий")
        return categories
    except FileNotFoundError:
        logger.error(f"Файл {json_file} не найден")
        return set()
    except json.JSONDecodeError:
        logger.error(f"Ошибка при чтении JSON файла")
        return set()

def generate_categories_sql() -> str:
    """Генерирует SQL запрос для вставки категорий"""
    categories = get_unique_categories()
    if not categories:
        return ""
    
    values = ", ".join([f"('{category}')" for category in categories])
    sql = f"""
    INSERT INTO categories (name) VALUES {values}
    ON DUPLICATE KEY UPDATE name=VALUES(name);
    """
    
    logger.info("SQL запрос для вставки категорий сгенерирован")
    return sql

if __name__ == "__main__":
    # Настройка логгера
    logging.basicConfig(level=logging.INFO)
    
    # Получаем SQL запрос
    sql = generate_categories_sql()
    print("\nSQL запрос для вставки категорий:")
    print(sql)