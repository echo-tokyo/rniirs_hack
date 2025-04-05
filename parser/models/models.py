from datetime import datetime
import re
from typing import Optional, Dict, List, Any
from bs4 import BeautifulSoup, Tag
from requests import get
from config import MONTHS

class RscfParser:
    def __init__(self) -> None:
        self.base_url: str = "https://rscf.ru/news/"
        self.categories: Dict[str, str] = {
            'all': '',
            'media': 'media/',
            'found': 'found/',
            'interview': 'interview/',
            'release': 'release/'
        }
        self.months: Dict[str, str] = MONTHS

    def get_news(self, category: str = 'all', initial_load: bool = False, pages: int = 10) -> List[Dict[str, str]]:
        """
        Получает новости с сайта РНФ
        
        Args:
            category: категория новостей
            initial_load: флаг первоначальной загрузки
            pages: количество страниц для первоначальной загрузки
        """
        if category not in self.categories:
            raise ValueError(f"Неверная категория. Доступные категории: {', '.join(self.categories.keys())}")
        
        all_news_items: List[Dict[str, str]] = []
        
        # Определяем количество страниц для парсинга
        pages_to_parse = pages if initial_load else 1
        
        for page in range(1, pages_to_parse + 1):
            url = f"{self.base_url}?PAGEN_2={page}"
            response = get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            for item in soup.find_all('div', class_='news-item'):
                news = {
                    'title': item.find('a', class_='news-title').text.strip(),
                    'category': item.find('a', class_='news-category').text.strip(),
                    'link': item.find('a', class_='news-title')['href']
                }
                all_news_items.append(news)
        
        return all_news_items
    
    def _process_links(self, element: Tag) -> str:
        """Обрабатывает текст и заменяет HTML ссылки на markdown формат"""
        text: str = element.text.strip()
        links: List[Tag] = element.find_all('a')
        
        if not links:
            return text
            
        for link in links:
            link_text: str = link.text.strip()
            link_url: str = link.get('href', '')
            
            if link_url.startswith('/'):
                link_url = f"https://rscf.ru{link_url}"
            elif not link_url.startswith(('http://', 'https://')):
                link_url = f"https://rscf.ru/{link_url}"
                
            text = text.replace(link_text, f"[{link_text}]({link_url})")
            
        return text

    def _parse_date(self, date_str: str, time_str: str) -> Optional[datetime]:
        """Преобразует строку с датой и временем в объект datetime"""
        if not date_str:
            return None
            
        day, month, year = re.match(r'(\d+)\s+(\w+),\s+(\d+)', date_str).groups()
        month_num: Optional[str] = self.months.get(month.lower())
        
        if not month_num:
            return None
            
        date_formatted: str = f"{day.zfill(2)}.{month_num}.{year}"
        
        if time_str:
            datetime_str: str = f"{date_formatted} {time_str}"
            try:
                return datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
            except ValueError:
                return None
        else:
            try:
                return datetime.strptime(date_formatted, "%d.%m.%Y")
            except ValueError:
                return None

    def get_news_detail(self, url: str) -> Dict[str, Any]:
        if not url.startswith('http'):
            if url.startswith('/'):
                url = f"https://rscf.ru{url}"
            else:
                url = f"https://rscf.ru/{url}"
                
        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        news_datetime: Optional[datetime] = None
        date_time_elem = (
            soup.find('span', class_='news-date-time') or 
            soup.find('div', class_='news-date') or
            soup.find('div', class_='b-news-detail-date')
        )
        
        if date_time_elem:
            date_time_text: str = date_time_elem.text.strip()
            date_match = re.search(r'(\d+\s+\w+,\s+\d+)', date_time_text)
            time_match = re.search(r'(\d+:\d+)', date_time_text)
            
            date_str: str = date_match.group(1) if date_match else ""
            time_str: str = time_match.group(1) if time_match else ""
            
            news_datetime = self._parse_date(date_str, time_str)
        
        source_elem = soup.find('div', class_='news-detail-source')
        source: str = source_elem.find('a').text.strip() if source_elem and source_elem.find('a') else ""
        
        tags_block = soup.find('div', class_='b-news-detail-tags')
        category: str = tags_block.find('a').text.strip() if tags_block and tags_block.find('a') else ""
        
        markdown_content: List[str] = []
        
        intro = soup.find('div', class_='news-detail-intro')
        if intro:
            intro_text: str = self._process_links(intro)
            markdown_content.append(f"**{intro_text}**\n")
        
        content_block = soup.find('div', class_='b-news-detail-content')
        if content_block:
            for element in content_block.find_all(['p', 'blockquote']):
                if element.name == 'blockquote':
                    quote_text: str = self._process_links(element)
                    markdown_content.append(f"> {quote_text}\n")
                elif element.name == 'p' and not element.find_parent('blockquote'):
                    text: str = self._process_links(element)
                    if element.find('i'):
                        markdown_content.append(f"*{text}*\n")
                    else:
                        markdown_content.append(f"{text}\n")
        
        detail: Dict[str, Any] = {
            'date': news_datetime,
            'source': source,
            'content': '\n'.join(markdown_content)
        }
        
        return detail
