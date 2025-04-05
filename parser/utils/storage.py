import json
from datetime import datetime
from typing import Set, List, Dict, Any
from config import JSON_FILE, BASE_DIR
import os
import logging

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)

def load_processed_links(source: str) -> Set[str]:
    """Загружает список обработанных ссылок для конкретного источника"""
    try:
        with open(os.path.join(BASE_DIR, f'{source}_processed_links.json'), 'r') as f:
            data = json.load(f)
            return set(data['processed_links'])
    except FileNotFoundError:
        return set()
    
def save_json(data: Any, filepath: str) -> None:
    """Сохраняет данные в JSON файл с поддержкой datetime"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)

def save_processed_links(links: Set[str], source: str) -> None:
    """Сохраняет список обработанных ссылок для конкретного источника"""
    with open(os.path.join(BASE_DIR, f'{source}_processed_links.json'), 'w') as f:
        json.dump({'processed_links': list(links)}, f)

def send_to_database(news_items: List[Dict[str, Any]], is_update: bool = False) -> None:
    """Имитация отправки новостей в базу данных"""
    if is_update:
        print(f"Отправка {len(news_items)} новых новостей в БД...")
    else:
        print(f"Первичная отправка {len(news_items)} новостей в БД...")
    # Здесь будет код для отправки в БД

PARSER_STATE_FILE = os.path.join(BASE_DIR, 'parser_state.json')

def load_parser_state(source: str) -> bool:
    """Загружает состояние парсера для конкретного источника"""
    try:
        with open(os.path.join(BASE_DIR, f'{source}_state.json'), 'r') as f:
            state = json.load(f)
            return state.get('initial_load_completed', False)
    except FileNotFoundError:
        return False

def save_parser_state(initial_load_completed: bool, source: str) -> None:
    """Сохраняет состояние парсера для конкретного источника"""
    with open(os.path.join(BASE_DIR, f'{source}_state.json'), 'w') as f:
        json.dump({'initial_load_completed': initial_load_completed}, f)