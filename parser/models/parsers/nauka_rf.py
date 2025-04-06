import aiohttp
import logging
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
from bs4 import BeautifulSoup
import re
import json
import os
from mistralai import Mistral
from dotenv import load_dotenv
from ..base_parser import BaseParser

class NaukaRfParser(BaseParser):
    def __init__(self):
        super().__init__()
        # Загружаем переменные окружения
        load_dotenv()
        
        self.base_url = "https://xn--80aa3ak5a.xn--p1ai"
        self.api_url = f"{self.base_url}/news/?AJAX=Y&PAGEN_1={{}}&period=0"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Инициализация Mistral AI
        self.ML_API_URL = "http://classifier-api:8001/predict"
        
        self.session = None  # Добавляем атрибут для хранения сессии
        
        self.categories = [
            'Интервью', 'Физика и космос', 'Инженерные науки', 
            'Науки о Земле', 'Математика', 'Биология', 
            'Новости Фонда', 'Сельское хозяйство', 
            'Гуманитарные науки', 'СМИ о Фонде', 
            'Медицина', 'Химия и материалы'
        ]
        
        # Настройка логгера с отключенным выводом
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)  # Показывать только ошибки

        self.news_buffer = []
        self.batch_size = 10
        self._send_callback = None  # Добавляем атрибут для колбэка
        self._category_cache = {}  # Кэш для категорий

    @property
    def source_name(self) -> str:
        """Возвращает название источника новостей"""
        return "наука.рф"

    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()

    async def _parse_date(self, date_str: str) -> str:
        """
        Преобразует строку даты в формат YYYY-MM-DD
        Вход: "5 апреля 2025"
        Выход: "2025-04-05"
        """
        self.logger.debug(f"Парсинг даты: {date_str}")
        try:
            months = {
                'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04',
                'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
                'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
            }
            
            day, month, year = date_str.split()
            # Добавляем ведущий ноль к дню, если нужно
            day = day.zfill(2)
            month_num = months[month.lower()]
            
            result = f"{year}-{month_num}-{day}"
            self.logger.debug(f"Дата успешно преобразована: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Ошибка при парсинге даты {date_str}: {e}")
            return None

    async def _process_news_item(self, item: Dict) -> Dict:
        """Обрабатывает отдельную новость"""
        self.logger.info("=" * 50)
        self.logger.info("Обработка новой новости")
        
        # Получаем базовую информацию
        title = item['title']
        # self.logger.info(f"Заголовок: {title}")
        
        link = item['url']
        # self.logger.info(f"Ссылка: {link}")
        
        date = await self._parse_date(item['date'])
        # self.logger.info(f"Дата: {date}")
        
        # Определяем категорию
        category = await self._get_category(title)
        self.logger.info(f"Категория: {category}")
        
        # Формируем структуру новости
        news_item = {
            'title': title,
            'category': category,
            'link': link,
            'date': date,
            'author': 'наука.рф'
        }
        
        # Получаем детали новости
        url = f"{self.base_url}{link}"
        details = await self.get_news_detail(url)
        if details:
            news_item['description'] = details['description']
            # Выводим часть контента для проверки
            content_preview = details['description'][:100] + "..." if len(details['description']) > 100 else details['description']
            # self.logger.info(f"Контент (превью): {content_preview}")
        
        # Выводим итоговую структуру новости
        self.logger.info("Итоговая структура новости:")
        self.logger.info(json.dumps(news_item, ensure_ascii=False, indent=2))
        self.logger.info("=" * 50)
        
        return news_item

    def set_send_callback(self, callback):
        """Устанавливает функцию для отправки данных"""
        self._send_callback = callback

    async def _send_batch(self) -> bool:
        """Отправляет накопленный пакет новостей"""
        if len(self.news_buffer) >= self.batch_size and self._send_callback:
            batch = self.news_buffer[:self.batch_size]
            self.news_buffer = self.news_buffer[self.batch_size:]
            return await self._send_callback(batch)
        return True

    async def get_news(self, initial_load: bool = False, pages: int = 2) -> List[Dict]:
        """Получает список новостей с сайта наука.рф"""
        all_news = []
        current_page = 1
        
        try:
            while current_page <= pages:
                url = self.api_url.format(current_page)
                
                async with self.session.get(url) as response:
                    if response.status != 200:
                        self.logger.error(f"Ошибка при получении страницы {current_page}")
                        break
                        
                    data = await response.json()
                    if not data.get('ITEMS'):
                        break
                    
                    # Обработка каждой новости на странице
                    for item in data['ITEMS']:
                        processed_news = await self._process_news_item(item)
                        all_news.append(processed_news)
                        self.news_buffer.append(processed_news)
                        
                        # Отправляем пакет, если накопилось достаточно новостей
                        await self._send_batch()
                    
                    current_page += 1
                    
                    if not initial_load and current_page > 1:
                        break
                        
        except Exception as e:
            self.logger.error(f"Ошибка при получении новостей: {str(e)}")
            
        # Отправляем оставшиеся новости
        if self.news_buffer:
            await self._send_batch()
            self.news_buffer = []
            
        return all_news

    async def get_news_detail(self, url: str) -> Dict:
        """Получает детальную информацию о новости"""
        self.logger.info(f"Получение деталей новости: {url}")
        try:
            self.logger.debug(f"Отправка GET запроса к {url}")
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.logger.error(f"Ошибка при получении деталей новости: {response.status}")
                    return None
                
                html = await response.text()
                # self.logger.debug(f"Получен ответ, длина HTML: {len(html)}")
                soup = BeautifulSoup(html, 'html.parser')
                
                # Получаем заголовок
                title = soup.find('h1', class_='u-inner-header__title')
                title = title.text.strip() if title else ""
                # self.logger.debug(f"Найден заголовок: {title}")
                
                # Получаем дату
                date_elem = soup.find('time', class_='u-news-detail__date')
                date = await self._parse_date(date_elem.text.strip()) if date_elem else None
                # self.logger.debug(f"Найдена дата: {date}")
                
                # Получаем контент
                content_div = soup.find('div', class_='u-news-detail-page__text-content')
                if not content_div:
                    # self.logger.error("Не найден основной контент новости")
                    return None
                    
                markdown_content = []
                
                # Обработка интро
                intro = content_div.find('b')
                if intro:
                    intro_text = intro.text.strip()
                    markdown_content.append(f"**{intro_text}**\n")
                    # self.logger.debug("Обработан интро текст")
                
                # Обработка изображений и текста
                image_count = 0
                previous_was_image = False
                
                for element in content_div.find_all(['p', 'br', 'img-wyz']):
                    if element.name == 'img-wyz':
                        src = element.get('src', '')
                        if src:
                            image_count += 1
                            # self.logger.debug(f"Найдено изображение {image_count}: {src}")
                            if not previous_was_image:
                                markdown_content.append("")
                            markdown_content.append(f"![image]({src})")
                            previous_was_image = True
                    elif element.name == 'p':
                        text = element.text.strip()
                        if text:
                            if previous_was_image:
                                markdown_content.append("")
                            markdown_content.append(text)
                            previous_was_image = False
                
                # Объединяем контент с одним переносом строки между элементами
                content = '\n'.join(markdown_content)
                # Убираем множественные переносы строк (более двух)
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                result = {
                    'title': title,
                    'date': date,
                    'description': content
                }
                
                self.logger.info(f"Успешно обработана новость: {title}")
                return result
                
        except Exception as e:
            # self.logger.error(f"Ошибка при парсинге деталей новости {url}: {str(e)}", exc_info=True)
            return None

    async def _get_category(self, title: str) -> str:
        """Определяет категорию новости через API classifier-api"""
        # Проверяем кэш
        if title in self._category_cache:
            return self._category_cache[title]
        
        try:
            async with self.session.get(self.ML_API_URL) as response:
                if response.status != 200:
                    self.logger.error(f"Ошибка при получении деталей новости: {response.status}")
                    return "Новости Фонда"
                
                result = response.json()
                category = result.get("prediction", "Новости Фонда")
                
                # Валидация полученной категории
                return category
                
        except asyncio.TimeoutError:
            self.logger.warning("Таймаут при запросе к classifier-api")
            return "Новости Фонда"
        except aiohttp.ClientError as e:
            self.logger.warning(f"Ошибка соединения с classifier-api: {str(e)}")
            return "Новости Фонда"
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка: {str(e)}")
            return "Новости Фонда"

