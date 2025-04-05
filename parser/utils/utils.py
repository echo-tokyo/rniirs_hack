def format_news_item(news, detail):
    """Форматирует новость в единый объект"""
    return {
        'title': news['title'],
        'category': news['category'],
        'link': news['link'],
        'date': detail['date'],
        'source': detail['source'],
        'content': detail['content']
    }