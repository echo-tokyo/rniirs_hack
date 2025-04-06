import logging
import os
import asyncio
import json
import time

from models.parser_factory import ParserFactory
from config import BASE_DIR, AMOUNT_PAGES
from utils.database import send_to_database, save_to_csv

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',  # Упрощаем формат
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'parser.log')),
        logging.StreamHandler()
    ]
)

# Отключаем логи от других модулей
logging.getLogger('aiohttp').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('mistralai').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

# В начале файла добавим константу для пути к JSON файлам
JSON_DIR = os.path.join(BASE_DIR, 'json_objects')

def load_processed_links(source: str) -> set:
    """Загружает множество обработанных ссылок"""
    try:
        filepath = os.path.join(JSON_DIR, f"processed_links_{source}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return set(json.load(f))
    except Exception as e:
        logger.error(f"Ошибка при загрузке обработанных ссылок: {e}")
    return set()

def save_processed_links(links: set, source: str) -> None:
    """Сохраняет множество обработанных ссылок"""
    try:
        os.makedirs(JSON_DIR, exist_ok=True)  # Создаем директорию, если её нет
        filepath = os.path.join(JSON_DIR, f"processed_links_{source}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(list(links), f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при сохранении обработанных ссылок: {e}")

def load_parser_state(source: str) -> bool:
    """Загружает состояние парсера"""
    try:
        filepath = os.path.join(JSON_DIR, f"parser_state_{source}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f).get('initial_load_completed', False)
    except Exception as e:
        logger.error(f"Ошибка при загрузке состояния парсера: {e}")
    return False

def save_parser_state(state: bool, source: str) -> None:
    """Сохраняет состояние парсера"""
    try:
        os.makedirs(JSON_DIR, exist_ok=True)  # Создаем директорию, если её нет
        filepath = os.path.join(JSON_DIR, f"parser_state_{source}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({'initial_load_completed': state}, f)
    except Exception as e:
        logger.error(f"Ошибка при сохранении состояния парсера: {e}")

def save_json(items: list, filename: str) -> None:
    """Сохраняет новости в JSON файл"""
    try:
        os.makedirs(JSON_DIR, exist_ok=True)
        filepath = os.path.join(JSON_DIR, filename)
        
        # Убедимся, что все новости имеют правильные поля
        for item in items:
            if 'content' in item:
                item['description'] = item.pop('content')
            if 'source' in item:
                item['author'] = item.pop('source')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        logger.info(f"Сохранено {len(items)} новостей в {filepath}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении JSON: {e}")

class NewsBatcher:
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.news_buffer = []
        self.logger = logging.getLogger(__name__)

    async def add_news(self, news_items: list) -> None:
        """Добавляет новости в буфер и отправляет, если достигнут размер пакета"""
        self.news_buffer.extend(news_items)
        if len(self.news_buffer) >= self.batch_size:
            await self._send_batch()

    async def _send_batch(self) -> bool:
        """Отправляет пакет новостей"""
        if not self.news_buffer:
            return True

        batch = self.news_buffer[:self.batch_size]
        success = await send_to_database(batch)
        
        if success:
            self.news_buffer = self.news_buffer[self.batch_size:]
            return True
        return False

    async def flush(self) -> bool:
        """Отправляет все оставшиеся новости"""
        while self.news_buffer:
            if not await self._send_batch():
                return False
        return True

async def process_news_source(source: str):
    """Асинхронно обрабатывает новости из указанного источника"""
    try:
        parser = ParserFactory.get_parser(source)
        logger.info(f"[{source}] Начало обработки")
        
        # Загружаем обработанные ссылки и состояние
        processed_links = load_processed_links(source)
        initial_load_completed = load_parser_state(source)
        
        async with parser as p:
            if not initial_load_completed:
                # Первичная загрузка - используем пакетную обработку
                logger.info(f"[{source}] Первичная загрузка данных")
                parser.set_send_callback(save_to_csv)  # Включаем пакетную отправку
                current_news = await p.get_news(initial_load=True, pages=AMOUNT_PAGES)
                
                if current_news:
                    # Сохраняем все ссылки
                    processed_links.update(news['link'] for news in current_news)
                    save_processed_links(processed_links, source)
                    
                    # Сохраняем состояние
                    save_parser_state(True, source)
                    logger.info(f"[{source}] Первичная загрузка завершена. Обработано {len(current_news)} новостей")
                
            else:
                # Обычный режим - проверяем только новые новости
                logger.info(f"[{source}] Проверка новых новостей")
                parser.set_send_callback(None)  # Отключаем пакетную отправку
                current_news = await p.get_news(initial_load=False, pages=1)
                
                if current_news:
                    # Фильтруем только новые новости
                    new_news = [
                        news for news in current_news 
                        if news['link'] not in processed_links
                    ]
                    
                    if new_news:
                        # Отправляем новые новости одним запросом
                        await send_to_database(new_news)
                        
                        # Обновляем список обработанных ссылок
                        processed_links.update(news['link'] for news in new_news)
                        save_processed_links(processed_links, source)
                        
                        logger.info(f"[{source}] Найдено {len(new_news)} новых новостей")
                    else:
                        logger.info(f"[{source}] Новых новостей нет")
                
            # Сохраняем текущие новости в JSON для проверки
            if current_news:
                save_json(
                    current_news,
                    f"news_{source}.json"
                )
                
    except Exception as e:
        logger.error(f"[{source}] Ошибка: {str(e)}")

async def main():
    """Основная функция для запуска парсеров"""
    sources = ['rscf']
    tasks = [process_news_source(source) for source in sources]
    await asyncio.gather(*tasks)

def run_parser():
    """Функция для запуска парсера"""
    
    start_time = time.time()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Парсер остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
    finally:
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        print(f"Время выполнения парсинга: {duration} сек.")


if __name__ == "__main__":
    run_parser()
    