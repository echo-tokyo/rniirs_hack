import logging
import os
from models.parser_factory import ParserFactory
from utils.storage import (
    load_processed_links, 
    save_processed_links, 
    send_to_database, 
    save_json,
    load_parser_state,
    save_parser_state
)
from utils.utils import format_news_item
from config import BASE_DIR

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'parser.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_news_source(source: str):
    """Обрабатывает новости из указанного источника"""
    try:
        parser = ParserFactory.get_parser(source)
        logger.info(f"Начало обработки новостей из источника: {parser.source_name}")
        
        processed_links = load_processed_links(source)
        initial_load_completed = load_parser_state(source)
        
        # Получаем новости (при первом запуске - 10 страниц, потом только первую)
        current_news = parser.get_news(initial_load=not initial_load_completed, pages=10)
        
        if not current_news:
            logger.error("Не удалось получить новости")
            return
        
        logger.info(f"Получено новостей: {len(current_news)}")
        
        # Получаем новости только с первой страницы для отслеживания
        first_page_news = parser.get_news(initial_load=False, pages=1)
        first_page_links = {news['link'] for news in first_page_news}
        
        # Обновляем processed_links, оставляя только ссылки с первой страницы
        processed_links = processed_links & first_page_links
        
        # Проверяем новые новости из всех полученных страниц
        new_news = [news for news in current_news if news['link'] not in processed_links]
        
        if new_news:
            logger.info(f"Найдено {len(new_news)} новых новостей")
            new_news_items = []
            
            for i, news in enumerate(new_news, 1):
                logger.info(f"Обработка новой новости {i}/{len(new_news)}: {news['title'][:50]}...")
                try:
                    detail = parser.get_news_detail(news['link'])
                    news_item = format_news_item(news, detail)                
                    new_news_items.append(news_item)
                    save_json(new_news_items, os.path.join(BASE_DIR, "news_example.json"))
                    
                    # Добавляем в processed_links только если новость с первой страницы
                    if news['link'] in first_page_links:
                        processed_links.add(news['link'])
                except Exception as e:
                    logger.error(f"Ошибка при обработке новости: {str(e)}")
                    continue
            
            if new_news_items:
                save_processed_links(processed_links, source)
                send_to_database(new_news_items, is_update=True)
                
                # Сохраняем состояние после успешного первого парсинга
                if not initial_load_completed:
                    save_parser_state(True, source)
                
                logger.info(f"Обработано и отправлено {len(new_news_items)} новых новостей")
        else:
            logger.info("Новых новостей не найдено")
    except Exception as e:
        logger.error(f"Ошибка при обработке источника {source}: {str(e)}")

def main():
    # Список источников для обработки
    sources = ['rscf']  # Добавляйте новые источники сюда
    
    for source in sources:
        process_news_source(source)

if __name__ == "__main__":
    main()
    