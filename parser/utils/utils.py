def format_news_item(news, detail):
    """Форматирует новость в единый объект"""
    return {
        'title': news['title'],
        'category': news['category'],
        'link': news['link'],
        'date': detail['date'],
        'author': detail['author'],
        'description': detail['description']
    }