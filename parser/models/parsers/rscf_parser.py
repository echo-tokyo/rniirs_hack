from datetime import datetime
import re
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup, Tag
from requests import get

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
    
    @property
    def source_name(self) -> str:
        return "РНФЦ"

    def get_news(self, initial_load: bool = False, pages: int = 10) -> List[Dict[str, str]]:
        if initial_load:
            pages_to_parse = pages
        else:
            pages_to_parse = 1
            
        all_news_items = []
        
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

    def get_news_detail(self, url: str) -> Dict[str, Any]:
        if not url.startswith('http'):
            if url.startswith('/'):
                url = f"https://rscf.ru{url}"
            else:
                url = f"https://rscf.ru/{url}"
                
        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        news_datetime = None
        date_time_elem = (
            soup.find('span', class_='news-date-time') or 
            soup.find('div', class_='news-date') or
            soup.find('div', class_='b-news-detail-date')
        )
        
        if date_time_elem:
            date_time_text = date_time_elem.text.strip()
            date_match = re.search(r'(\d+\s+\w+,\s+\d+)', date_time_text)
            time_match = re.search(r'(\d+:\d+)', date_time_text)
            
            date_str = date_match.group(1) if date_match else ""
            time_str = time_match.group(1) if time_match else ""
            
            news_datetime = self._parse_date(date_str, time_str)
        
        source_elem = soup.find('div', class_='news-detail-source')
        source = source_elem.find('a').text.strip() if source_elem and source_elem.find('a') else ""
        
        markdown_content = []
        
        intro = soup.find('div', class_='news-detail-intro')
        if intro:
            intro_text = self._process_links(intro)
            markdown_content.append(f"**{intro_text}**\n")
        
        content_block = soup.find('div', class_='b-news-detail-content')
        if content_block:
            for element in content_block.find_all(['p', 'blockquote']):
                if element.name == 'blockquote':
                    quote_text = self._process_links(element)
                    markdown_content.append(f"> {quote_text}\n")
                elif element.name == 'p' and not element.find_parent('blockquote'):
                    text = self._process_links(element)
                    if element.find('i'):
                        markdown_content.append(f"*{text}*\n")
                    else:
                        markdown_content.append(f"{text}\n")
        
        detail = {
            'date': news_datetime,
            'source': source,
            'content': '\n'.join(markdown_content)
        }
        
        return detail

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

    def _parse_date(self, date_str: str, time_str: str) -> Optional[datetime]:
        if not date_str:
            return None
            
        day, month, year = re.match(r'(\d+)\s+(\w+),\s+(\d+)', date_str).groups()
        month_num = self.months.get(month.lower())
        
        if not month_num:
            return None
            
        date_formatted = f"{day.zfill(2)}.{month_num}.{year}"
        
        if time_str:
            datetime_str = f"{date_formatted} {time_str}"
            try:
                return datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
            except ValueError:
                return None
        else:
            try:
                return datetime.strptime(date_formatted, "%d.%m.%Y")
            except ValueError:
                return None 