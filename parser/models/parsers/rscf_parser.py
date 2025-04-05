from datetime import datetime
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup, Tag
from requests import get
import asyncio
import aiohttp
import logging
import json

from ..base_parser import BaseParser
from config import MONTHS

class RscfParser(BaseParser):
    def __init__(self):
        self.base_url = "https://rscf.ru/news/"
        self.categories = {
            'all': '',
            'media': 'media/',
            'found': 'found/',
            'interview': 'interview/',
            'release': 'release/'
        }
        self.months = MONTHS
        self.session = None
        self.news_buffer = []
        self.batch_size = 10
        self._send_callback = None  # Добавляем атрибут для колбэка
        
        # Настройка логгера с отключенным выводом
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)  # Показывать только ошибки
    
    def set_send_callback(self, callback):
        """Устанавливает функцию для отправки данных"""
        self._send_callback = callback

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    @property
    def source_name(self) -> str:
        return "РНФЦ"

    async def _send_batch(self) -> bool:
        """Отправляет накопленный пакет новостей"""
        if len(self.news_buffer) >= self.batch_size and self._send_callback:
            batch = self.news_buffer[:self.batch_size]
            self.news_buffer = self.news_buffer[self.batch_size:]
            return await self._send_callback(batch)
        return True

    async def _process_news_item(self, news: Dict, details: Dict) -> Dict:
        """Обрабатывает и объединяет базовую информацию с деталями новости"""
        if details:
            news.update(details)  # Обновляем базовую информацию деталями
            return news
        return None

    async def get_news(self, initial_load: bool = False, pages: int = 10) -> List[Dict[str, str]]:
        """Получает и обрабатывает новости"""
        all_news = []
        pages_to_parse = pages if initial_load else 1
        
        try:
            async with aiohttp.ClientSession() as session:
                for page in range(1, pages_to_parse + 1):
                    url = f"{self.base_url}?PAGEN_2={page}"
                    self.logger.info(f"Обработка страницы {page}: {url}")
                    
                    async with session.get(url) as response:
                        if response.status != 200:
                            self.logger.error(f"Ошибка при получении страницы {page}: {response.status}")
                            continue
                            
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        
                        news_items = []
                        for item in soup.find_all('div', class_='news-item'):
                            news = {
                                'title': item.find('a', class_='news-title').text.strip(),
                                'category': item.find('a', class_='news-category').text.strip(),
                                'link': item.find('a', class_='news-title')['href'],
                                'author': 'РНФЦ'  # Добавляем автора сразу
                            }
                            news_items.append(news)
                        
                        # Асинхронно получаем детали для всех новостей на странице
                        tasks = [self.get_news_detail(news['link']) for news in news_items]
                        details_list = await asyncio.gather(*tasks)
                        
                        # Объединяем базовую информацию с деталями
                        for news, details in zip(news_items, details_list):
                            processed_news = await self._process_news_item(news, details)
                            if processed_news:
                                all_news.append(processed_news)
                                self.news_buffer.append(processed_news)
                                
                                # Отправляем пакет, если накопилось достаточно новостей
                                await self._send_batch()
                
        except Exception as e:
            self.logger.error(f"Ошибка при получении новостей: {str(e)}")
        
        # Отправляем оставшиеся новости
        if self.news_buffer and self._send_callback:
            await self._send_callback(self.news_buffer)
            self.news_buffer = []
        
        return all_news

    async def get_news_detail(self, url: str) -> Dict[str, Any]:
        """Получает детальную информацию о новости"""
        if not url.startswith('http'):
            url = f"https://rscf.ru{url if url.startswith('/') else f'/{url}'}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        self.logger.error(f"Ошибка при получении деталей новости: {response.status}")
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    
                    # Получаем дату
                    date_time_elem = (
                        soup.find('span', class_='news-date-time') or 
                        soup.find('div', class_='news-date') or
                        soup.find('div', class_='b-news-detail-date')
                    )
                    
                    news_datetime = None
                    if date_time_elem:
                        date_time_text = date_time_elem.text.strip()
                        date_match = re.search(r'(\d+\s+\w+,\s+\d+)', date_time_text)
                        if date_match:
                            news_datetime = self._parse_date(date_match.group(1))
                    
                    # Формируем контент
                    markdown_content = []
                    
                    # Обработка главного изображения
                    main_image = soup.find('div', class_='b-news-detail-picture')
                    if main_image and main_image.find('img'):
                        img_src = main_image.find('img').get('src', '')
                        if img_src:
                            if img_src.startswith('/'):
                                img_src = f"https://rscf.ru{img_src}"
                            markdown_content.append(f"![image]({img_src})")
                    
                    # Обработка интро
                    intro = soup.find('div', class_='news-detail-intro')
                    if intro:
                        intro_text = self._process_links(intro)
                        markdown_content.append(f"**{intro_text}**")
                    
                    # Обработка основного контента
                    content_block = soup.find('div', class_='b-news-detail-content')
                    if content_block:
                        for element in content_block.find_all(['p', 'blockquote', 'img', 'div']):
                            if element.name in ['img', 'div'] and element.get('class') == ['b-news-detail-picture']:
                                img = element if element.name == 'img' else element.find('img')
                                if img and img.get('src'):
                                    img_src = img.get('src')
                                    if img_src.startswith('/'):
                                        img_src = f"https://rscf.ru{img_src}"
                                    markdown_content.append(f"![image]({img_src})")
                            elif element.name == 'blockquote':
                                quote_text = self._process_links(element)
                                markdown_content.append(f"> {quote_text}")
                            elif element.name == 'p' and not element.find_parent('blockquote'):
                                text = self._process_links(element)
                                markdown_content.append(text)
                    
                    # Объединяем контент
                    content = '\n\n'.join(markdown_content)
                    
                    return {
                        'date': news_datetime,
                        'description': content,
                        'author': 'РНФЦ'
                    }
                    
        except Exception as e:
            self.logger.error(f"Ошибка при парсинге деталей новости {url}: {str(e)}")
            return None

    def _process_links(self, element: Tag) -> str:
        text = element.text.strip()
        links = element.find_all('a')
        
        if not links:
            return text
            
        for link in links:
            link_text = link.text.strip()
            link_url = link.get('href', '')
            
            if link_url.startswith('/'):
                link_url = f"https://rscf.ru{link_url}"
            elif not link_url.startswith(('http://', 'https://')):
                link_url = f"https://rscf.ru/{link_url}"
                
            text = text.replace(link_text, f"[{link_text}]({link_url})")
            
        return text

    def _parse_date(self, date_str: str) -> str:
        """
        Преобразует строку даты в формат DD-MM-YYYY
        Вход: "5 апреля, 2025"
        Выход: "05-04-2025"
        """
        if not date_str:
            return None
            
        try:
            day, month, year = re.match(r'(\d+)\s+(\w+),\s+(\d+)', date_str).groups()
            month_num = self.months.get(month.lower())
            
            if not month_num:
                return None
            
            # Добавляем ведущий ноль к дню и месяцу
            return f"{day.zfill(2)}-{month_num.zfill(2)}-{year}"
        except Exception as e:
            return None 

# Пример использования:
# async def main():
#     async with RscfParser() as parser:
#         news = await parser.get_news(initial_load=True, pages=3)
#         print(f"Всего обработано новостей: {len(news)}")
#         for item in news:
#             print(json.dumps(item, ensure_ascii=False, indent=2))

# if __name__ == "__main__":
#     asyncio.run(main()) 