from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable


class BaseParser(ABC):
    """Абстрактный базовый класс для всех парсеров новостей"""
    
    @abstractmethod
    def get_news(self, **kwargs) -> List[Dict[str, str]]:
        """Получает список новостей"""
        pass
    
    @abstractmethod
    def get_news_detail(self, url: str) -> Dict[str, Any]:
        """Получает детальную информацию о новости"""
        pass
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Возвращает название источника новостей"""
        pass

    @abstractmethod
    def set_send_callback(self, callback: Callable):
        """Устанавливает функцию для отправки данных"""
        pass 