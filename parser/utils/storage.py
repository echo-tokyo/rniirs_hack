import json
from datetime import datetime
from typing import Set, List, Dict, Any
from config import JSON_FILE

def load_processed_links() -> Set[str]:
    """Загружает список уже обработанных ссылок"""
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data: Dict[str, List[str]] = json.load(f)
            return set(data['processed_links'])
    except FileNotFoundError:
        return set()

def save_processed_links(links: Set[str]) -> None:
    """Сохраняет список обработанных ссылок"""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump({'processed_links': list(links)}, f, ensure_ascii=False, indent=2)

def send_to_database(news_items: List[Dict[str, Any]], is_update: bool = False) -> None:
    """Имитация отправки новостей в базу данных"""
    if is_update:
        print(f"Отправка {len(news_items)} новых новостей в БД...")
    else:
        print(f"Первичная отправка {len(news_items)} новостей в БД...")
    # Здесь будет код для отправки в БД