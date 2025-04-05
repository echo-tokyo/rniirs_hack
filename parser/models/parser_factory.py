from typing import Dict, Type
from .base_parser import BaseParser
from .parsers.rscf_parser import RscfParser

class ParserFactory:
    """Фабрика для создания парсеров"""
    
    _parsers: Dict[str, Type[BaseParser]] = {
        'rscf': RscfParser,
        # Здесь будут добавляться новые парсеры
        # 'other_source': OtherSourceParser,
    }
    
    @classmethod
    def get_parser(cls, source: str) -> BaseParser:
        """Создает и возвращает парсер для указанного источника"""
        parser_class = cls._parsers.get(source)
        if not parser_class:
            raise ValueError(f"Парсер для источника '{source}' не найден")
        return parser_class()
    
    @classmethod
    def register_parser(cls, source: str, parser_class: Type[BaseParser]) -> None:
        """Регистрирует новый парсер"""
        cls._parsers[source] = parser_class 